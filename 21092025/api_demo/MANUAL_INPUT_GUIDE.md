# Manual Input Guide - When Scraping Fails

## The Problem

Web scraping Google Maps doesn't always work because Google loads data via JavaScript. But you can see the data in your browser!

## The Solution: Manual Input Endpoint

Simply copy the data from Google Maps and paste it into the API!

## Example: Quán Bụi Garden

### What You See in Google Maps:
```
Quán Bụi Garden
4.4 ⭐ (2,217 reviews)
Vietnamese restaurant
55A Ngô Quang Huy, Thảo Điền, Thủ Đức, Thành phố Hồ Chí Minh 70000
```

### API Request:

```bash
curl -X POST "http://localhost:8000/predict-manual" \
  -H "Content-Type: application/json" \
  -d '{
    "google_maps_url": "https://www.google.com/maps/place/Qu%C3%A1n+B%E1%BB%A5i+Garden/@10.8046882,106.7360579,18.45z",
    "rating": 4.4,
    "reviews": 2217,
    "category": "Vietnamese restaurant",
    "address": "55A Ngô Quang Huy, Thảo Điền, Thủ Đức, Thành phố Hồ Chí Minh 70000"
  }'
```

### Response:

```json
{
  "success": true,
  "place_info": {
    "name": "Quán Bụi Garden",
    "latitude": 10.8046882,
    "longitude": 106.7360579,
    "address": "55A Ngô Quang Huy, Thảo Điền, Thủ Đức, Thành phố Hồ Chí Minh 70000",
    "rating": 4.4,
    "reviews": 2217,
    "category": "Vietnamese restaurant"
  },
  "prediction": 1,
  "prediction_label": "Beer Seller",
  "confidence": 0.8523,
  "confidence_percentage": "85.23%",
  "risk_level": "Very High Potential",
  "recommendation": "✓ Highly recommended for beer sales...",
  "all_features": {
    "avg_rating": 4.4,
    "reviews_number": 2217,
    "last_avg_rating": 4.4,
    "last_1_reviews_number": 665.1,
    "last_2_reviews_number": 1108.5,
    "latitude": 10.8046882,
    "longitude": 106.7360579,
    "location_type_resolved": "Vietnamese restaurant",
    "province_name": "Thành phố Hồ Chí Minh",
    "ward_name": "Thảo Điền",
    "idx_r9_hex": "8965b5643c7ffff",
    "name": "Quán Bụi Garden",
    "tfidf_applied": true
  },
  "features_summary": {
    "total_features": "11 base + ~9000 TF-IDF text features",
    "data_source": "Manual input"
  }
}
```

## Quick Copy-Paste Template

```bash
curl -X POST "http://localhost:8000/predict-manual" \
  -H "Content-Type: application/json" \
  -d '{
    "google_maps_url": "PASTE_URL_HERE",
    "rating": 0.0,
    "reviews": 0,
    "category": "Restaurant",
    "address": "PASTE_ADDRESS_HERE"
  }'
```

## Python Example

```python
import requests

data = {
    "google_maps_url": "YOUR_URL",
    "rating": 4.4,
    "reviews": 2217,
    "category": "Vietnamese restaurant",
    "address": "55A Ngô Quang Huy, Thảo Điền, Thủ Đức, Thành phố Hồ Chí Minh"
}

response = requests.post("http://localhost:8000/predict-manual", json=data)
result = response.json()

print(f"Prediction: {result['prediction_label']}")
print(f"Confidence: {result['confidence_percentage']}")
print(f"All features: {result['all_features']}")
```

## Optional Fields

You can provide only some fields:

```json
{
  "google_maps_url": "...",
  "rating": 4.4,
  "reviews": 2217
  // category and address will be inferred/defaulted
}
```

## Try It Now!

1. **Start the API**: `python main.py`
2. **Open**: http://localhost:8000/docs
3. **Find**: `/predict-manual` endpoint
4. **Click**: "Try it out"
5. **Paste**: Your data
6. **Execute**: Get instant prediction with ALL features!

---

## Why This Works Better

✅ **Accurate Data**: You provide exactly what you see  
✅ **All Features**: Gets all 11 base features correctly  
✅ **Fast**: No waiting for scraping/JavaScript  
✅ **Reliable**: Always works, no scraping failures  

This is the **recommended approach** until we add Google Places API integration or Selenium support.

