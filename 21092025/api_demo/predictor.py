"""
Beer Sales Prediction Model Predictor
Loads trained model and makes predictions on new POI data
Follows EXACT same preprocessing as beer_sales_prediction_2.ipynb
"""
import joblib
import pandas as pd
import numpy as np
import re
import h3
import sys
from typing import Dict, Tuple, Optional
from pathlib import Path

# Import shared tokenizer for pickle compatibility
sys.path.insert(0, str(Path(__file__).parent))
from utils import simple_tokenizer
from aggregated_features import AggregatedFeaturesCalculator
from sales_assignment import SalesAssignmentMapper

# Make tokenizer available to __main__ for pickle compatibility
import __main__
__main__.simple_tokenizer = simple_tokenizer


class BeerSalesPredictor:
    """Predictor class for beer sales potential"""
    
    def __init__(self, model_dir: str = "../model"):
        """
        Initialize predictor by loading saved models
        
        Args:
            model_dir: Directory containing saved models
        """
        self.model_dir = Path(model_dir)
        self.model = None
        self.tfidf = None
        self.metadata = None
        self.aggregated_features = None
        
        # Quantity prediction models
        self.quantity_model = None
        self.quantity_tfidf = None
        self.quantity_preprocessor = None
        self.quantity_metadata = None
        
        # Sales assignment mapper
        self.sales_assignment = None
        
        self.load_models()
        self.load_quantity_models()
        self.load_aggregated_features()
        self.load_sales_assignment()
    
    def load_models(self):
        """Load all required models and metadata"""
        try:
            # Load LightGBM classifier
            model_path = self.model_dir / "lightgbm_classifier.pkl"
            self.model = joblib.load(model_path)
            print(f"✓ Loaded model from {model_path}")
            
            # Load TF-IDF vectorizer
            tfidf_path = self.model_dir / "tfidf_vectorizer.pkl"
            self.tfidf = joblib.load(tfidf_path)
            print(f"✓ Loaded TF-IDF vectorizer from {tfidf_path}")
            
            # Load metadata
            metadata_path = self.model_dir / "model_metadata.pkl"
            self.metadata = joblib.load(metadata_path)
            print(f"✓ Loaded metadata from {metadata_path}")
            
            print(f"\nModel Performance:")
            print(f"  - Test AUC: {self.metadata.get('test_auc', 'N/A'):.4f}")
            print(f"  - Test Accuracy: {self.metadata.get('test_accuracy', 'N/A'):.4f}")
            
        except Exception as e:
            raise Exception(f"Error loading models: {e}")
    
    def load_quantity_models(self):
        """Load quantity prediction models (quartile prediction)"""
        try:
            # Load quantity LightGBM classifier
            quantity_model_path = self.model_dir / "quantity_lightgbm_classifier.pkl"
            if quantity_model_path.exists():
                self.quantity_model = joblib.load(quantity_model_path)
                print(f"✓ Loaded quantity model from {quantity_model_path}")
                
                # Load quantity TF-IDF vectorizer
                quantity_tfidf_path = self.model_dir / "quantity_tfidf_vectorizer.pkl"
                self.quantity_tfidf = joblib.load(quantity_tfidf_path)
                print(f"✓ Loaded quantity TF-IDF vectorizer from {quantity_tfidf_path}")
                
                # Load quantity preprocessor
                quantity_preprocessor_path = self.model_dir / "quantity_preprocessor.pkl"
                self.quantity_preprocessor = joblib.load(quantity_preprocessor_path)
                print(f"✓ Loaded quantity preprocessor from {quantity_preprocessor_path}")
                
                # Load quantity metadata
                quantity_metadata_path = self.model_dir / "quantity_model_metadata.pkl"
                self.quantity_metadata = joblib.load(quantity_metadata_path)
                print(f"✓ Loaded quantity metadata from {quantity_metadata_path}")
            else:
                print("⚠️ Quantity model not found - quantity prediction will be unavailable")
        except Exception as e:
            print(f"⚠️ Warning: Could not load quantity models: {e}")
            self.quantity_model = None
    
    def load_aggregated_features(self):
        """Load aggregated features calculator"""
        try:
            self.aggregated_features = AggregatedFeaturesCalculator(data_dir=str(self.model_dir.parent))
            self.aggregated_features.load_stats(str(self.model_dir / "aggregated_stats.json"))
            print("✓ Loaded aggregated features")
        except Exception as e:
            print(f"⚠️ Warning: Could not load aggregated features: {e}")
            self.aggregated_features = None
    
    def load_sales_assignment(self):
        """Load sales assignment mapper"""
        try:
            sales_data_dir = self.model_dir / "sale_assgined"
            if sales_data_dir.exists():
                self.sales_assignment = SalesAssignmentMapper(data_dir=str(sales_data_dir))
                print("✓ Loaded sales assignment mapper")
            else:
                print(f"⚠️ Warning: Sales assignment data directory not found: {sales_data_dir}")
        except Exception as e:
            print(f"⚠️ Warning: Could not load sales assignment: {e}")
            self.sales_assignment = None
    
    def get_sales_assignment(self, place_data: Dict[str, any]) -> Dict:
        """
        Get sales assignment for a place
        
        Args:
            place_data: Dictionary containing place information (category, latitude, longitude, idx_r9_hex)
            
        Returns:
            Dictionary with channel, territory, and sales rep information
        """
        if self.sales_assignment is None:
            return {
                'channel': None,
                'territory': None,
                'sales_rep': None,
                'hex_id': None
            }
        
        category = place_data.get('category') or place_data.get('location_type_resolved')
        latitude = place_data.get('latitude')
        longitude = place_data.get('longitude')
        hex_id = place_data.get('idx_r9_hex')
        
        return self.sales_assignment.get_sales_assignment(
            category=category,
            latitude=latitude,
            longitude=longitude,
            hex_id=hex_id
        )
    
    def get_aggregated_features(self, place_data: Dict[str, any]) -> Dict:
        """
        Get aggregated features for category and hexagon
        
        Args:
            place_data: Dictionary containing place information
            
        Returns:
            Dictionary with aggregated statistics
        """
        if self.aggregated_features is None:
            return {}
        
        category = place_data.get('category') or place_data.get('location_type_resolved')
        hex_id = place_data.get('idx_r9_hex')
        ward = place_data.get('ward_name')
        
        result = {
            'category_features': None,
            'hexagon_features': None,
            'ward_features': None,
            'overall_stats': self.aggregated_features.get_overall_stats(),
            'all_category_stats': None  # Include all categories for comparison
        }
        
        # Get category stats
        if category:
            cat_features = self.aggregated_features.get_category_features(category)
            if cat_features:
                result['category_features'] = cat_features
        
        # Get all category stats for comparison (if Restaurant category)
        if category and category.lower() == 'restaurant':
            if self.aggregated_features.aggregated_stats:
                result['all_category_stats'] = self.aggregated_features.aggregated_stats.get('category_stats', {})
        
        # Get hexagon stats
        if hex_id:
            hex_features = self.aggregated_features.get_hexagon_features(str(hex_id))
            if hex_features:
                result['hexagon_features'] = hex_features
        
        # Get ward stats
        if ward:
            ward_features = self.aggregated_features.get_ward_features(ward)
            if ward_features:
                result['ward_features'] = ward_features
        
        return result
    
    def preprocess_single_place(self, place_data: Dict[str, any]) -> pd.DataFrame:
        """
        Preprocess a single place following EXACT same steps as notebook
        
        Args:
            place_data: Dictionary with place information from URL parser
                - place_name: str
                - latitude: float
                - longitude: float
                - avg_rating: float (or None)
                - reviews_number: int (or None)
                - category: str (or None)
                - ward_name: str (or None)
                - address: str (or None)
            
        Returns:
            DataFrame with all features ready for prediction
        """
        # Step 1: Create base features (same as notebook Cell 10)
        numeric_features = [
            "avg_rating", "reviews_number", "last_avg_rating",
            "last_1_reviews_number", "last_2_reviews_number",
            'latitude', 'longitude'
        ]
        categorical_features = [
            "location_type_resolved", "province_name", "ward_name",
            "idx_r9_hex"
        ]
        
        # Fill in features from scraped data with defaults if missing
        rating = place_data.get('avg_rating') or 4.0
        reviews = place_data.get('reviews_number') or 0
        
        # Use scraped historical features or calculate defaults
        last_avg_rating = place_data.get('last_avg_rating') or rating
        last_1_reviews_number = place_data.get('last_1_reviews_number') or (reviews * 0.3 if reviews else 0)
        last_2_reviews_number = place_data.get('last_2_reviews_number') or (reviews * 0.5 if reviews else 0)
        
        # Calculate H3 hex index - resolution 9, same as training data
        idx_r9 = place_data.get('idx_r9_hex')  # Use pre-calculated if available
        if not idx_r9:
            lat = place_data.get('latitude')
            lon = place_data.get('longitude')
            if lat and lon and lat != 0 and lon != 0:
                try:
                    # Use latlng_to_cell (h3-py v4.x) - resolution 9, same as aggregated_features
                    idx_r9 = h3.latlng_to_cell(lat, lon, 9)
                except:
                    idx_r9 = None
        
        # Create feature dict with all required features
        features = {
            # Numeric features
            'avg_rating': rating,
            'reviews_number': reviews,
            'last_avg_rating': last_avg_rating,
            'last_1_reviews_number': last_1_reviews_number,
            'last_2_reviews_number': last_2_reviews_number,
            'latitude': place_data.get('latitude', 10.8),
            'longitude': place_data.get('longitude', 106.7),
            # Categorical features
            'location_type_resolved': place_data.get('category', 'Restaurant'),
            'province_name': place_data.get('province_name', 'Thành phố Hồ Chí Minh'),
            'ward_name': place_data.get('ward_name') or 'Unknown',
            'idx_r9_hex': idx_r9
        }
        
        # Create DataFrame
        X = pd.DataFrame([features])
        
        # Step 2: Convert categorical features to category dtype (Cell 11)
        for col in categorical_features:
            X[col] = X[col].astype('category')
        
        # Step 3: Apply TF-IDF to name (Cell 12)
        name = place_data.get('place_name', '')
        if self.tfidf and name:
            try:
                # Transform the name using the fitted TF-IDF
                tfidf_matrix = self.tfidf.transform([name])
                tfidf_features = self.tfidf.get_feature_names_out()
                embedding_df = pd.DataFrame(
                    tfidf_matrix.toarray(), 
                    columns=[f'tfidf_{w}' for w in tfidf_features]
                )
                
                # Concatenate with X
                X = pd.concat([X, embedding_df], axis=1)
            except Exception as e:
                print(f"Warning: Could not process TF-IDF features: {e}")
        
        # Step 4: Clean column names (Cell 13)
        # Remove special characters from column names
        new_names = {col: re.sub(r'[^A-Za-z0-9_]+', '', col) for col in X.columns}
        new_n_list = list(new_names.values())
        
        # Handle duplicate names by appending index
        new_names = {
            col: f'{new_col}_{i}' if new_col in new_n_list[:i] else new_col 
            for i, (col, new_col) in enumerate(new_names.items())
        }
        X = X.rename(columns=new_names)
        
        return X
    
    def predict(self, place_data: Dict[str, any]) -> Tuple[int, float, Dict]:
        """
        Predict beer sales potential for a place
        
        Args:
            place_data: Dictionary containing place information from URL parser
            
        Returns:
            Tuple of (prediction, probability, detailed_results)
        """
        # Preprocess features following notebook steps
        X = self.preprocess_single_place(place_data)
        
        # Make prediction
        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0]
        
        # Probability of being a beer seller (class 1)
        prob_seller = probability[1]
        
        # Special rule: Karaoke should always be predicted as Beer Seller with high confidence (>90%)
        category = place_data.get('category') or place_data.get('location_type_resolved', '')
        if category and 'Karaoke' in str(category):
            prediction = 1  # Force Beer Seller
            prob_seller = 0.95  # Set high confidence (95%)
            print(f"✓ Override: Karaoke category -> Beer Seller (95% confidence)")
        
        # Create detailed results
        results = {
            'prediction': int(prediction),
            'prediction_label': 'Beer Seller' if prediction == 1 else 'Non-Beer Seller',
            'confidence': float(prob_seller),
            'confidence_percentage': f"{prob_seller * 100:.2f}%",
            'risk_level': self._get_risk_level(prob_seller),
            'recommendation': self._get_recommendation(prob_seller, place_data)
        }
        
        return int(prediction), float(prob_seller), results
    
    def get_tfidf_feature_importance(self, place_name: str, top_n: int = 10) -> Dict:
        """
        Get TF-IDF feature importance for a specific place name
        
        Args:
            place_name: The place name to analyze
            top_n: Number of top features to return
            
        Returns:
            Dictionary with TF-IDF analysis including:
            - present_terms: Terms from the name that are in the model
            - important_terms: Terms with high feature importance
            - top_terms: Overall top important terms (even if not in this name)
        """
        if not self.model or not self.tfidf or not place_name:
            return {
                'present_terms': [],
                'important_terms': [],
                'top_terms': [],
                'analysis': 'TF-IDF analysis not available'
            }
        
        try:
            # Get feature importance from model
            feature_importance = self.model.feature_importances_
            
            # Get feature names - need to reconstruct them
            # The model was trained with: preprocessed features + TF-IDF features
            # We need to get the column names after preprocessing
            
            # Transform the place name to get which TF-IDF features are present
            tfidf_matrix = self.tfidf.transform([place_name])
            tfidf_features = self.tfidf.get_feature_names_out()
            tfidf_values = tfidf_matrix.toarray()[0]
            
            # Tokenize the place name to see what tokens are present
            from utils import simple_tokenizer
            tokens = simple_tokenizer(place_name)
            
            # Create a mapping of TF-IDF feature names to their indices in the full feature set
            # This is tricky because we need to know the order of features in the model
            # For now, we'll use a simpler approach: analyze TF-IDF terms that are present
            
            # Get indices where TF-IDF values are non-zero (terms present in this name)
            present_indices = tfidf_values.nonzero()[0]
            present_terms = [tfidf_features[i] for i in present_indices]
            present_tfidf_values = tfidf_values[present_indices]
            
            # Since we can't easily map to exact feature importance indices,
            # we'll use TF-IDF values as a proxy for importance
            # Terms with higher TF-IDF values are more important for this specific name
            
            # Sort by TF-IDF value
            term_importance = list(zip(present_terms, present_tfidf_values))
            term_importance.sort(key=lambda x: x[1], reverse=True)
            
            # Get top terms
            top_present_terms = [term for term, score in term_importance[:top_n] if score > 0]
            
            # Also get overall important terms (common terms that typically indicate beer sales)
            # We'll identify these by looking at common Vietnamese/English restaurant terms
            common_beer_terms = ['quán', 'nhà hàng', 'restaurant', 'bar', 'pub', 'cafe', 
                                'bistro', 'grill', 'bbq', 'beer', 'brewery', 'tavern']
            
            # Find which common terms are in the name
            name_lower = place_name.lower()
            found_common_terms = [term for term in common_beer_terms if term in name_lower]
            
            return {
                'present_terms': present_terms[:20],  # All terms present
                'important_terms': top_present_terms,  # Top terms by TF-IDF value
                'common_beer_terms_found': found_common_terms,
                'tokens': tokens,
                'analysis': f'Found {len(present_terms)} TF-IDF features in this name'
            }
        except Exception as e:
            print(f"Error analyzing TF-IDF features: {e}")
            return {
                'present_terms': [],
                'important_terms': [],
                'top_terms': [],
                'analysis': f'Error: {str(e)}'
            }
    
    def _get_risk_level(self, probability: float) -> str:
        """Categorize confidence into risk levels"""
        if probability >= 0.8:
            return "Very High Potential"
        elif probability >= 0.6:
            return "High Potential"
        elif probability >= 0.4:
            return "Medium Potential"
        elif probability >= 0.2:
            return "Low Potential"
        else:
            return "Very Low Potential"
    
    def _get_recommendation(self, probability: float, place_data: Dict) -> str:
        """Generate recommendation based on prediction"""
        if probability >= 0.7:
            return f"✓ Highly recommended for beer sales. Strong indicators present (Rating: {place_data.get('avg_rating', 'N/A')}, Reviews: {place_data.get('reviews_number', 'N/A')})."
        elif probability >= 0.5:
            return f"⚠ Moderate potential for beer sales. Consider location and competition factors."
        else:
            return f"✗ Low potential for beer sales. May not be suitable for this product category."
    
    def preprocess_for_quantity(self, place_data: Dict[str, any]) -> pd.DataFrame:
        """
        Preprocess features for quantity prediction (same as binary but uses quantity preprocessor)
        
        Args:
            place_data: Dictionary containing place information
            
        Returns:
            Preprocessed DataFrame ready for quantity model
        """
        if self.quantity_preprocessor is None:
            raise ValueError("Quantity preprocessor not loaded")
        
        # Use same feature extraction as binary prediction
        numeric_features = [
            "avg_rating", "reviews_number", "last_avg_rating",
            "last_1_reviews_number", "last_2_reviews_number",
            'latitude', 'longitude'
        ]
        categorical_features = [
            "location_type_resolved", "province_name", "ward_name",
            "idx_r9_hex"
        ]
        
        # Create feature dict
        features = {
            'avg_rating': place_data.get('avg_rating', 0) or 0,
            'reviews_number': place_data.get('reviews_number', 0) or 0,
            'last_avg_rating': place_data.get('last_avg_rating') or place_data.get('avg_rating', 0) or 0,
            'last_1_reviews_number': place_data.get('last_1_reviews_number', 0) or 0,
            'last_2_reviews_number': place_data.get('last_2_reviews_number', 0) or 0,
            'latitude': place_data.get('latitude', 10.8),
            'longitude': place_data.get('longitude', 106.7),
            'location_type_resolved': place_data.get('category', 'Restaurant'),
            'province_name': place_data.get('province_name', 'Thành phố Hồ Chí Minh'),
            'ward_name': place_data.get('ward_name') or 'Unknown',
            'idx_r9_hex': place_data.get('idx_r9_hex') or None
        }
        
        # Calculate hexagon if missing
        if not features['idx_r9_hex']:
            lat = features['latitude']
            lon = features['longitude']
            if lat and lon and lat != 0 and lon != 0:
                try:
                    features['idx_r9_hex'] = h3.latlng_to_cell(lat, lon, 9)
                except:
                    features['idx_r9_hex'] = None
        
        # Create DataFrame
        X = pd.DataFrame([features])
        
        # Set categorical types
        for col in categorical_features:
            X[col] = X[col].astype('category')
        
        return X
    
    def predict_quantity(self, place_data: Dict[str, any]) -> Optional[Dict]:
        """
        Predict beer selling quantity quartile (Q1, Q2, Q3, Q4)
        
        Args:
            place_data: Dictionary containing place information
            
        Returns:
            Dictionary with quartile prediction and details, or None if model not available
        """
        if self.quantity_model is None or self.quantity_tfidf is None or self.quantity_preprocessor is None:
            return None
        
        try:
            # Preprocess features
            X_numeric_cat = self.preprocess_for_quantity(place_data)
            
            # Process text feature
            name = place_data.get('place_name', '')
            if name and self.quantity_tfidf:
                X_text_tfidf = self.quantity_tfidf.transform([name])
            else:
                # Create empty TF-IDF matrix with same dimensions
                X_text_tfidf = self.quantity_tfidf.transform([""])
            
            # Transform numeric/categorical features
            X_processed = self.quantity_preprocessor.transform(X_numeric_cat)
            
            # Combine features
            from scipy.sparse import hstack
            X_combined = hstack([X_processed, X_text_tfidf])
            
            # Make prediction
            quartile_pred = self.quantity_model.predict(X_combined)[0]
            quartile_proba = self.quantity_model.predict_proba(X_combined)[0]
            
            # Get quartile labels
            quartile_labels = {1: 'Q1 (Lowest)', 2: 'Q2', 3: 'Q3', 4: 'Q4 (Highest)'}
            quartile_label = quartile_labels.get(int(quartile_pred), f'Q{int(quartile_pred)}')
            
            # Get bin edges for interpretation
            bin_edges = self.quantity_metadata.get('bin_edges', [])
            
            return {
                'quartile': int(quartile_pred),
                'quartile_label': quartile_label,
                'probabilities': {
                    'Q1': float(quartile_proba[0]),
                    'Q2': float(quartile_proba[1]),
                    'Q3': float(quartile_proba[2]),
                    'Q4': float(quartile_proba[3])
                },
                'confidence': float(max(quartile_proba)),
                'bin_edges': bin_edges,
                'interpretation': self._get_quantity_interpretation(int(quartile_pred), bin_edges)
            }
        except Exception as e:
            print(f"Error predicting quantity: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _get_quantity_interpretation(self, quartile: int, bin_edges: list) -> str:
        """Get interpretation of quartile prediction"""
        if not bin_edges or len(bin_edges) < 5:
            return f"Predicted quartile: Q{quartile}"
        
        quartile_labels = {
            1: 'Q1 (Lowest)',
            2: 'Q2',
            3: 'Q3',
            4: 'Q4 (Highest)'
        }
        
        label = quartile_labels.get(quartile, f'Q{quartile}')
        
        if quartile == 1:
            return f"{label}: Expected volume in lowest 25% (≤ {bin_edges[1]:.2f})"
        elif quartile == 2:
            return f"{label}: Expected volume in 25-50% range ({bin_edges[1]:.2f} - {bin_edges[2]:.2f})"
        elif quartile == 3:
            return f"{label}: Expected volume in 50-75% range ({bin_edges[2]:.2f} - {bin_edges[3]:.2f})"
        else:  # quartile == 4
            return f"{label}: Expected volume in highest 25% (≥ {bin_edges[3]:.2f})"


if __name__ == "__main__":
    # Test the predictor
    print("Testing Beer Sales Predictor...\n")
    
    predictor = BeerSalesPredictor()
    
    # Test with sample features
    test_place = {
        'place_name': 'Quán Bụi Garden',
        'latitude': 10.805121,
        'longitude': 106.735759,
        'avg_rating': 4.3,
        'reviews_number': 150,
        'category': 'Restaurant',
        'ward_name': 'Phường 10',
        'address': 'Thành phố Hồ Chí Minh'
    }
    
    prediction, probability, results = predictor.predict(test_place)
    
    print("\n=== Prediction Results ===")
    print(f"Place: {test_place['place_name']}")
    print(f"Prediction: {results['prediction_label']}")
    print(f"Confidence: {results['confidence_percentage']}")
    print(f"Risk Level: {results['risk_level']}")
    print(f"Recommendation: {results['recommendation']}")
