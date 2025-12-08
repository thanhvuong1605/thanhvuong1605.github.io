"""
Configuration settings for the Beer Sales Prediction API
"""
import os
from pathlib import Path


# API Server Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# Model Configuration
MODEL_DIR = os.getenv("MODEL_DIR", "../model")
MODEL_PATH = Path(MODEL_DIR)

# Google API Configuration (Optional)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", None)

# Feature Configuration
NUMERIC_FEATURES = [
    "avg_rating", 
    "reviews_number", 
    "last_avg_rating",
    "last_1_reviews_number", 
    "last_2_reviews_number",
    "latitude", 
    "longitude"
]

CATEGORICAL_FEATURES = [
    "location_type_resolved", 
    "province_name", 
    "ward_name",
    "idx_r9_hex"
]

# Default values for missing features
DEFAULT_VALUES = {
    'avg_rating': 4.0,
    'reviews_number': 10,
    'last_avg_rating': 4.0,
    'province_name': 'Thành phố Hồ Chí Minh',
    'location_type_resolved': 'Restaurant'
}

# Confidence thresholds
CONFIDENCE_THRESHOLDS = {
    'very_high': 0.8,
    'high': 0.6,
    'medium': 0.4,
    'low': 0.2
}



