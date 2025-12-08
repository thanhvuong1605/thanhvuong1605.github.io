# 🍺 Beer Sales Potential Predictor API

An API that predicts the beer-selling potential of Points of Interest (POI) from Google Maps links using machine learning.

## 🚀 Features

- **URL Parsing**: Extracts place name, coordinates, and metadata from Google Maps URLs
- **ML Prediction**: Uses trained LightGBM model to predict beer-selling potential
- **RESTful API**: FastAPI-based REST API with automatic documentation
- **Streamlit Web Interface**: Beautiful interactive demo with analytics and visualizations
- **Confidence Scoring**: Provides confidence percentages and risk levels
- **Batch Processing**: Support for multiple URLs at once

## 📋 Prerequisites

- Python 3.8+
- Trained model files in `../model/` directory:
  - `lightgbm_classifier.pkl`
  - `tfidf_vectorizer.pkl`
  - `model_metadata.pkl`

## 🔧 Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Verify model files**:
Ensure the following files exist in `../model/`:
- `lightgbm_classifier.pkl`
- `tfidf_vectorizer.pkl`
- `model_metadata.pkl`

## 🎯 Usage

### Option 1: Streamlit Web Interface (Recommended for Demo)

Start the interactive web interface:

```bash
# Terminal 1: Start the API
python main.py

# Terminal 2: Start Streamlit
streamlit run streamlit_demo.py
```

The Streamlit app will open at `http://localhost:8501` with a beautiful UI for:
- Input Google Maps URLs
- View predictions with analytics
- Interactive visualizations
- Prediction history

See [STREAMLIT_DEMO.md](STREAMLIT_DEMO.md) for detailed guide.

### Option 2: API Server Only

```bash
python main.py
```

The API will start at `http://localhost:8000`

### Access API Documentation

Open your browser and go to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### 1. Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_info": {
    "test_auc": 0.8676,
    "test_accuracy": 0.8262,
    "num_features": 528
  }
}
```

### 2. Predict Single POI
```bash
POST /predict
Content-Type: application/json

{
  "google_maps_url": "https://www.google.com/maps/place/Qu%C3%A1n+B%E1%BB%A5i+Garden/@10.8046882,106.7360579,18.45z/data=!4m6!3m5!1s0x317526176671636b:0x471be660ffc59db!8m2!3d10.805121!4d106.735759",
  "google_api_key": null
}
```

**Response:**
```json
{
  "success": true,
  "place_info": {
    "name": "Quán Bụi Garden",
    "latitude": 10.805121,
    "longitude": 106.735759,
    "address": "N/A",
    "rating": 4.0,
    "reviews": 10,
    "category": "Restaurant"
  },
  "prediction": 1,
  "prediction_label": "Beer Seller",
  "confidence": 0.82,
  "confidence_percentage": "82.00%",
  "risk_level": "Very High Potential",
  "recommendation": "✓ Highly recommended for beer sales. Strong indicators present.",
  "features_used": {
    "avg_rating": 4.0,
    "reviews_number": 10,
    "location_type": "Restaurant",
    "latitude": 10.805121,
    "longitude": 106.735759,
    "h3_index": "8965b5643c7ffff"
  }
}
```

### 3. Batch Prediction
```bash
POST /predict-batch
Content-Type: application/json

{
  "urls": [
    "https://www.google.com/maps/place/...",
    "https://www.google.com/maps/place/..."
  ],
  "google_api_key": null
}
```

## 🧪 Testing

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Predict
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "google_maps_url": "https://www.google.com/maps/place/Qu%C3%A1n+B%E1%BB%A5i+Garden/@10.8046882,106.7360579,18.45z/data=!4m6!3m5!1s0x317526176671636b:0x471be660ffc59db!8m2!3d10.805121!4d106.735759"
  }'
```

### Using Python Requests

```python
import requests

url = "http://localhost:8000/predict"
data = {
    "google_maps_url": "https://www.google.com/maps/place/Qu%C3%A1n+B%E1%BB%A5i+Garden/@10.8046882,106.7360579,18.45z/data=!4m6!3m5!1s0x317526176671636b:0x471be660ffc59db!8m2!3d10.805121!4d106.735759"
}

response = requests.post(url, json=data)
print(response.json())
```

### Using the Test Script

```bash
python test_api.py
```

## 📊 Prediction Output

The API returns:
- **prediction**: 0 (Non-Beer Seller) or 1 (Beer Seller)
- **confidence**: Probability score (0-1)
- **risk_level**: 
  - Very High Potential (≥80%)
  - High Potential (60-80%)
  - Medium Potential (40-60%)
  - Low Potential (20-40%)
  - Very Low Potential (<20%)
- **recommendation**: Actionable advice based on prediction

## 🔑 Google Places API (Optional)

For better accuracy, you can provide a Google Places API key to fetch real-time data:

```json
{
  "google_maps_url": "...",
  "google_api_key": "YOUR_GOOGLE_API_KEY"
}
```

This will fetch:
- Actual ratings and review counts
- Business categories
- Address and phone number

## 🏗️ Architecture

```
api_demo/
├── main.py              # FastAPI application
├── predictor.py         # Model loading and prediction
├── url_parser.py        # Google Maps URL parsing
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── test_api.py         # Test script
```

## 📈 Model Information

- **Model Type**: LightGBM Classifier
- **Features**: 528 features including:
  - Numeric: ratings, reviews, coordinates
  - Categorical: location type, province, ward, H3 index
  - Text: TF-IDF of place name
- **Performance**: 
  - AUC: 0.8676
  - Accuracy: 82.62%

## 🐛 Troubleshooting

### Model not found
Ensure model files are in the correct location (`../model/`)

### URL parsing errors
The URL must be a valid Google Maps place link with coordinates

### Low confidence predictions
Without Google API key, the system uses default values which may affect accuracy

## 📝 License

Internal use - Heineken Project

## 👥 Contact

For questions or issues, contact the development team.



