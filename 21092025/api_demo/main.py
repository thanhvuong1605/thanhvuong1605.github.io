"""
FastAPI application for Beer Sales Prediction
Predicts beer-selling potential from Google Maps POI links
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, validator
from typing import Optional, Dict
import uvicorn

from url_parser import (
    parse_google_maps_url, 
    scrape_place_details_from_google,
    extract_ward_from_address,
    extract_province_from_address,
    infer_category_from_name
)
from predictor import BeerSalesPredictor


# Initialize FastAPI app
app = FastAPI(
    title="Beer Sales Potential Predictor API",
    description="API to predict beer-selling potential of POIs from Google Maps links",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor (load models once at startup)
predictor = None

@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    global predictor
    print("\n🚀 Starting Beer Sales Prediction API...")
    try:
        predictor = BeerSalesPredictor(model_dir="../model")
        print("✓ Models loaded successfully!\n")
    except Exception as e:
        print(f"✗ Error loading models: {e}")
        raise


# Request/Response Models
class PredictionRequest(BaseModel):
    """Request model for prediction"""
    google_maps_url: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "google_maps_url": "https://www.google.com/maps/place/Qu%C3%A1n+B%E1%BB%A5i+Garden/@10.8046882,106.7360579,18.45z/data=!4m6!3m5!1s0x317526176671636b:0x471be660ffc59db!8m2!3d10.805121!4d106.735759"
            }
        }


class ManualPredictionRequest(BaseModel):
    """Request model with manual data input (for when scraping fails)"""
    google_maps_url: str
    rating: Optional[float] = None
    reviews: Optional[int] = None
    category: Optional[str] = None
    address: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "google_maps_url": "https://www.google.com/maps/place/...",
                "rating": 4.4,
                "reviews": 2217,
                "category": "Vietnamese restaurant",
                "address": "55A Ngô Quang Huy, Thảo Điền, Thủ Đức, Thành phố Hồ Chí Minh 70000"
            }
        }


class PredictionResponse(BaseModel):
    """Response model for prediction"""
    success: bool
    place_info: Dict
    prediction: int
    prediction_label: str
    confidence: float
    confidence_percentage: str
    risk_level: str
    recommendation: str
    all_features: Dict  # All features used by model
    features_summary: Dict  # Summary of key features
    aggregated_features: Optional[Dict] = None  # Aggregated stats for category/hexagon
    quantity_prediction: Optional[Dict] = None  # Quantity quartile prediction
    tfidf_analysis: Optional[Dict] = None  # TF-IDF feature analysis
    sales_assignment: Optional[Dict] = None  # Sales territory and rep assignment


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    model_info: Optional[Dict] = None


# API Endpoints
@app.get("/", response_model=Dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Beer Sales Potential Predictor API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST) - Auto scrape from URL",
            "predict_manual": "/predict-manual (POST) - Provide data manually (RECOMMENDED)",
            "predict_batch": "/predict-batch (POST) - Multiple URLs",
            "docs": "/docs - Interactive API documentation"
        },
        "note": "Web scraping may not always work. Use /predict-manual for reliable results!"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    model_loaded = predictor is not None
    model_info = None
    
    if model_loaded and predictor.metadata:
        model_info = {
            "test_auc": predictor.metadata.get('test_auc'),
            "test_accuracy": predictor.metadata.get('test_accuracy'),
            "num_features": len(predictor.metadata.get('feature_names', []))
        }
    
    return {
        "status": "healthy" if model_loaded else "unhealthy",
        "model_loaded": model_loaded,
        "model_info": model_info
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_beer_sales(request: PredictionRequest):
    """
    Predict beer sales potential from Google Maps POI link
    
    Args:
        request: PredictionRequest containing google_maps_url
        
    Returns:
        PredictionResponse with prediction results
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Step 1: Scrape Google Maps URL for all details
        print(f"\n📍 Processing: {request.google_maps_url}")
        place_data = scrape_place_details_from_google(request.google_maps_url)
        
        if not place_data['latitude'] or not place_data['longitude']:
            raise HTTPException(
                status_code=400, 
                detail="Could not extract coordinates from URL. Please provide a valid Google Maps place link."
            )
        
        print(f"✓ Scraped: {place_data['place_name']} @ ({place_data['latitude']}, {place_data['longitude']})")
        
        # Step 2: Extract ward and province from address
        if place_data.get('address'):
            ward = extract_ward_from_address(place_data['address'])
            province = extract_province_from_address(place_data['address'])
            place_data['ward_name'] = ward
            place_data['province_name'] = province
        else:
            place_data['ward_name'] = None
            place_data['province_name'] = 'Thành phố Hồ Chí Minh'  # Default
        
        # Step 3: Infer category if not scraped
        if not place_data.get('category'):
            place_data['category'] = infer_category_from_name(
                place_data['place_name'], 
                place_data.get('category')
            )
        
        # Step 3.5: Calculate H3 index early (needed for aggregated features)
        # Always calculate from coordinates - resolution 9 (same as training data)
        import h3
        h3_index = None
        lat = place_data.get('latitude')
        lon = place_data.get('longitude')
        
        if lat and lon and lat != 0 and lon != 0:
            try:
                # Use latlng_to_cell (h3-py v4.x) - resolution 9
                h3_index = h3.latlng_to_cell(lat, lon, 9)
                place_data['idx_r9_hex'] = h3_index
                print(f"✓ Calculated hexagon: {h3_index}")
            except Exception as e:
                print(f"⚠️ Error calculating hexagon: {e}")
                place_data['idx_r9_hex'] = None
        else:
            print(f"⚠️ Missing coordinates: lat={lat}, lon={lon}")
            place_data['idx_r9_hex'] = None
        
        # Step 3.6: Get aggregated features to use as fallback for missing ratings
        aggregated_features = predictor.get_aggregated_features(place_data)
        
        # Step 3.7: Use aggregated features' ratings as fallback if scraping failed
        if not place_data.get('avg_rating') or place_data.get('avg_rating') is None:
            # Try to get rating from category and hexagon averages
            category_rating = None
            hexagon_rating = None
            
            if aggregated_features and aggregated_features.get('category_features'):
                category_rating = aggregated_features['category_features'].get('avg_rating')
            
            if aggregated_features and aggregated_features.get('hexagon_features'):
                hexagon_rating = aggregated_features['hexagon_features'].get('avg_rating')
            
            # Average the two if both available, otherwise use whichever is available
            if category_rating and hexagon_rating:
                fallback_rating = (category_rating + hexagon_rating) / 2
                place_data['avg_rating'] = fallback_rating
                place_data['reviews_number'] = place_data.get('reviews_number', 0) or (
                    aggregated_features.get('category_features', {}).get('avg_reviews', 0) if aggregated_features else 0
                )
                print(f"✓ Using fallback rating from aggregated features: {fallback_rating:.2f} (Category: {category_rating:.2f}, Hexagon: {hexagon_rating:.2f})")
            elif category_rating:
                place_data['avg_rating'] = category_rating
                place_data['reviews_number'] = place_data.get('reviews_number', 0) or (
                    aggregated_features.get('category_features', {}).get('avg_reviews', 0) if aggregated_features else 0
                )
                print(f"✓ Using category average rating: {category_rating:.2f}")
            elif hexagon_rating:
                place_data['avg_rating'] = hexagon_rating
                place_data['reviews_number'] = place_data.get('reviews_number', 0) or (
                    aggregated_features.get('hexagon_features', {}).get('avg_reviews', 0) if aggregated_features else 0
                )
                print(f"✓ Using hexagon average rating: {hexagon_rating:.2f}")
        
        # Recalculate temporal features if we updated rating
        if place_data.get('avg_rating'):
            place_data['last_avg_rating'] = place_data.get('avg_rating')
            reviews = place_data.get('reviews_number', 0)
            place_data['last_1_reviews_number'] = reviews * 0.3 if reviews else 0
            place_data['last_2_reviews_number'] = reviews * 0.5 if reviews else 0
        
        print(f"✓ Features extracted:")
        print(f"   - Rating: {place_data.get('avg_rating', 'N/A')} | Reviews: {place_data.get('reviews_number', 0)}")
        print(f"   - Category: {place_data.get('category', 'N/A')}")
        print(f"   - Province: {place_data.get('province_name', 'N/A')}")
        print(f"   - Ward: {place_data.get('ward_name', 'N/A')}")
        print(f"   - H3 Hexagon: {h3_index or 'N/A'}")
        
        # Step 4: Make prediction (predictor will handle preprocessing exactly like notebook)
        print("🤖 Running prediction...")
        prediction, probability, results = predictor.predict(place_data)
        
        print(f"✓ Prediction: {results['prediction_label']} ({results['confidence_percentage']})")
        
        # Step 5: Get aggregated features (already computed, but refresh to ensure latest)
        aggregated_features = predictor.get_aggregated_features(place_data)
        
        # Step 6: Get TF-IDF feature analysis
        tfidf_analysis = None
        if place_data.get('place_name'):
            tfidf_analysis = predictor.get_tfidf_feature_importance(place_data.get('place_name'))
        
        # Step 7: Get quantity prediction (if model is available and prediction is beer seller)
        quantity_prediction = None
        if prediction == 1:  # Only predict quantity for beer sellers
            quantity_prediction = predictor.predict_quantity(place_data)
            if quantity_prediction:
                print(f"✓ Quantity prediction: {quantity_prediction['quartile_label']} (Confidence: {quantity_prediction['confidence']*100:.1f}%)")
        
        # Step 7.5: Get sales assignment
        sales_assignment = None
        if predictor.sales_assignment:
            place_data['idx_r9_hex'] = h3_index  # Ensure hex_id is set
            sales_assignment = predictor.get_sales_assignment(place_data)
            if sales_assignment.get('sales_rep'):
                print(f"✓ Sales assignment: {sales_assignment['channel']} -> {sales_assignment['territory']} -> {sales_assignment['sales_rep']['srname']}")
            elif sales_assignment.get('territory'):
                print(f"✓ Sales territory: {sales_assignment['channel']} -> {sales_assignment['territory']} (sales rep not found)")
            elif sales_assignment.get('channel'):
                hex_id = sales_assignment.get('hex_id', 'N/A')
                print(f"⚠ Sales channel: {sales_assignment['channel']} (territory not found for hex_id: {hex_id})")
            else:
                print(f"⚠ Sales assignment: Category '{place_data.get('category')}' not mapped to channel")
        
        # Step 8: Return results with ALL features
        return PredictionResponse(
            success=True,
            place_info={
                'name': place_data.get('place_name', 'Unknown'),
                'latitude': place_data.get('latitude'),
                'longitude': place_data.get('longitude'),
                'address': place_data.get('address', 'N/A'),
                'rating': place_data.get('avg_rating'),
                'reviews': place_data.get('reviews_number', 0),
                'category': place_data.get('category')
            },
            prediction=results['prediction'],
            prediction_label=results['prediction_label'],
            confidence=results['confidence'],
            confidence_percentage=results['confidence_percentage'],
            risk_level=results['risk_level'],
            recommendation=results['recommendation'],
            all_features={
                # Numeric features
                'avg_rating': place_data.get('avg_rating'),
                'reviews_number': place_data.get('reviews_number', 0),
                'last_avg_rating': place_data.get('last_avg_rating'),
                'last_1_reviews_number': place_data.get('last_1_reviews_number', 0),
                'last_2_reviews_number': place_data.get('last_2_reviews_number', 0),
                'latitude': place_data.get('latitude'),
                'longitude': place_data.get('longitude'),
                # Categorical features
                'location_type_resolved': place_data.get('category'),
                'province_name': place_data.get('province_name'),
                'ward_name': place_data.get('ward_name'),
                'idx_r9_hex': place_data.get('idx_r9_hex') or h3_index,
                # Text feature
                'name': place_data.get('place_name'),
                'tfidf_applied': True  # Name was processed through TF-IDF
            },
            features_summary={
                'total_features': '11 base + ~9000 TF-IDF text features',
                'numeric_count': 7,
                'categorical_count': 4,
                'text_embeddings': 'TF-IDF applied to place name'
            },
            aggregated_features=aggregated_features,
            quantity_prediction=quantity_prediction,
            tfidf_analysis=tfidf_analysis,
            sales_assignment=sales_assignment
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict-manual", response_model=PredictionResponse)
async def predict_with_manual_data(request: ManualPredictionRequest):
    """
    Predict beer sales potential with manually provided data
    Use this when web scraping fails to get the data
    
    Args:
        request: ManualPredictionRequest with URL and manual data
        
    Returns:
        PredictionResponse with prediction results
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Step 1: Parse URL for basic info
        print(f"\n📍 Processing (Manual Mode): {request.google_maps_url}")
        place_data = parse_google_maps_url(request.google_maps_url)
        
        if not place_data['latitude'] or not place_data['longitude']:
            raise HTTPException(
                status_code=400, 
                detail="Could not extract coordinates from URL"
            )
        
        # Step 2: Use manually provided data
        place_data['avg_rating'] = request.rating
        place_data['reviews_number'] = request.reviews
        place_data['category'] = request.category
        place_data['address'] = request.address
        
        # Calculate H3 index early - always from coordinates, resolution 9
        import h3
        h3_index = None
        lat = place_data.get('latitude')
        lon = place_data.get('longitude')
        
        if lat and lon and lat != 0 and lon != 0:
            try:
                # Use latlng_to_cell (h3-py v4.x) - resolution 9
                h3_index = h3.latlng_to_cell(lat, lon, 9)
                place_data['idx_r9_hex'] = h3_index
                print(f"✓ Calculated hexagon: {h3_index}")
            except Exception as e:
                print(f"⚠️ Error calculating hexagon: {e}")
                place_data['idx_r9_hex'] = None
        else:
            print(f"⚠️ Missing coordinates: lat={lat}, lon={lon}")
            place_data['idx_r9_hex'] = None
        
        # Get aggregated features for fallback
        aggregated_features = predictor.get_aggregated_features(place_data)
        
        # Use aggregated ratings as fallback if not provided
        if not place_data.get('avg_rating') or place_data.get('avg_rating') is None:
            category_rating = None
            hexagon_rating = None
            
            if aggregated_features and aggregated_features.get('category_features'):
                category_rating = aggregated_features['category_features'].get('avg_rating')
            
            if aggregated_features and aggregated_features.get('hexagon_features'):
                hexagon_rating = aggregated_features['hexagon_features'].get('avg_rating')
            
            if category_rating and hexagon_rating:
                place_data['avg_rating'] = (category_rating + hexagon_rating) / 2
                print(f"✓ Using fallback rating from aggregated features: {place_data['avg_rating']:.2f}")
            elif category_rating:
                place_data['avg_rating'] = category_rating
                print(f"✓ Using category average rating: {category_rating:.2f}")
            elif hexagon_rating:
                place_data['avg_rating'] = hexagon_rating
                print(f"✓ Using hexagon average rating: {hexagon_rating:.2f}")
        
        # Calculate temporal features
        if place_data.get('avg_rating'):
            place_data['last_avg_rating'] = place_data.get('avg_rating')
            reviews = place_data.get('reviews_number', 0) or (
                aggregated_features.get('category_features', {}).get('avg_reviews', 0) if aggregated_features else 0
            )
            place_data['reviews_number'] = reviews
            place_data['last_1_reviews_number'] = reviews * 0.3
            place_data['last_2_reviews_number'] = reviews * 0.5
        
        # Extract location from address
        if request.address:
            place_data['ward_name'] = extract_ward_from_address(request.address)
            place_data['province_name'] = extract_province_from_address(request.address)
        else:
            place_data['ward_name'] = None
            place_data['province_name'] = 'Thành phố Hồ Chí Minh'
        
        # Infer category if not provided
        if not place_data.get('category'):
            place_data['category'] = infer_category_from_name(place_data['place_name'], None)
        
        print(f"✓ Manual data provided:")
        print(f"   - Rating: {place_data.get('avg_rating', 'N/A')} | Reviews: {place_data.get('reviews_number', 0)}")
        print(f"   - Category: {place_data.get('category', 'N/A')}")
        print(f"   - Address: {place_data.get('address', 'N/A')}")
        print(f"   - H3 Hexagon: {h3_index or 'N/A'}")
        
        # Step 3: Make prediction
        print("🤖 Running prediction...")
        prediction, probability, results = predictor.predict(place_data)
        
        print(f"✓ Prediction: {results['prediction_label']} ({results['confidence_percentage']})")
        
        # Step 4: Get aggregated features (already computed, but refresh to ensure latest)
        aggregated_features = predictor.get_aggregated_features(place_data)
        
        # Step 5: Get TF-IDF feature analysis
        tfidf_analysis = None
        if place_data.get('place_name'):
            tfidf_analysis = predictor.get_tfidf_feature_importance(place_data.get('place_name'))
        
        # Step 6: Get quantity prediction (if model is available and prediction is beer seller)
        quantity_prediction = None
        if prediction == 1:  # Only predict quantity for beer sellers
            quantity_prediction = predictor.predict_quantity(place_data)
            if quantity_prediction:
                print(f"✓ Quantity prediction: {quantity_prediction['quartile_label']} (Confidence: {quantity_prediction['confidence']*100:.1f}%)")
        
        # Step 6.5: Get sales assignment
        sales_assignment = None
        if predictor.sales_assignment:
            place_data['idx_r9_hex'] = h3_index  # Ensure hex_id is set
            sales_assignment = predictor.get_sales_assignment(place_data)
            if sales_assignment.get('sales_rep'):
                print(f"✓ Sales assignment: {sales_assignment['channel']} -> {sales_assignment['territory']} -> {sales_assignment['sales_rep']['srname']}")
            elif sales_assignment.get('channel'):
                print(f"✓ Sales channel: {sales_assignment['channel']} (territory not found)")
        
        # Step 7: Return results
        return PredictionResponse(
            success=True,
            place_info={
                'name': place_data.get('place_name', 'Unknown'),
                'latitude': place_data.get('latitude'),
                'longitude': place_data.get('longitude'),
                'address': place_data.get('address', 'N/A'),
                'rating': place_data.get('avg_rating'),
                'reviews': place_data.get('reviews_number', 0),
                'category': place_data.get('category')
            },
            prediction=results['prediction'],
            prediction_label=results['prediction_label'],
            confidence=results['confidence'],
            confidence_percentage=results['confidence_percentage'],
            risk_level=results['risk_level'],
            recommendation=results['recommendation'],
            all_features={
                'avg_rating': place_data.get('avg_rating'),
                'reviews_number': place_data.get('reviews_number', 0),
                'last_avg_rating': place_data.get('last_avg_rating'),
                'last_1_reviews_number': place_data.get('last_1_reviews_number', 0),
                'last_2_reviews_number': place_data.get('last_2_reviews_number', 0),
                'latitude': place_data.get('latitude'),
                'longitude': place_data.get('longitude'),
                'location_type_resolved': place_data.get('category'),
                'province_name': place_data.get('province_name'),
                'ward_name': place_data.get('ward_name'),
                'idx_r9_hex': place_data.get('idx_r9_hex') or h3_index,
                'name': place_data.get('place_name'),
                'tfidf_applied': True
            },
            features_summary={
                'total_features': '11 base + ~9000 TF-IDF text features',
                'numeric_count': 7,
                'categorical_count': 4,
                'text_embeddings': 'TF-IDF applied to place name',
                'data_source': 'Manual input'
            },
            aggregated_features=aggregated_features,
            quantity_prediction=quantity_prediction,
            tfidf_analysis=tfidf_analysis,
            sales_assignment=sales_assignment
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict-batch")
async def predict_batch(urls: list[str]):
    """
    Predict beer sales potential for multiple POIs
    
    Args:
        urls: List of Google Maps URLs
        
    Returns:
        List of predictions
    """
    results = []
    
    for url in urls:
        try:
            request = PredictionRequest(google_maps_url=url)
            result = await predict_beer_sales(request)
            results.append(result.dict())
        except Exception as e:
            results.append({
                "success": False,
                "url": url,
                "error": str(e)
            })
    
    return {
        "total": len(urls),
        "successful": sum(1 for r in results if r.get('success', False)),
        "results": results
    }


if __name__ == "__main__":
    # Run the API
    print("\n" + "="*60)
    print("🍺 Beer Sales Potential Predictor API")
    print("="*60)
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )

