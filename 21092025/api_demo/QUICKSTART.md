# 🚀 Quick Start Guide

Get the Beer Sales Prediction API running in 5 minutes!

## Prerequisites

- ✅ Python 3.8 or higher
- ✅ Trained models in `../model/` directory
- ✅ Internet connection (for initial setup)

## Step 1: Installation

### Option A: Using the run script (Recommended)

**On macOS/Linux:**
```bash
./run.sh
```

**On Windows:**
```bash
run.bat
```

### Option B: Manual installation

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Start the API

```bash
python main.py
```

You should see:
```
🚀 Starting Beer Sales Prediction API...
✓ Models loaded successfully!

INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 3: Test the API

### Option 1: Use the test script
```bash
python test_api.py
```

### Option 2: Use the example script
```bash
python example_usage.py
```

### Option 3: Visit the interactive docs
Open your browser: **http://localhost:8000/docs**

### Option 4: Use cURL
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "google_maps_url": "https://www.google.com/maps/place/Qu%C3%A1n+B%E1%BB%A5i+Garden/@10.8046882,106.7360579,18.45z/data=!4m6!3m5!1s0x317526176671636b:0x471be660ffc59db!8m2!3d10.805121!4d106.735759"
  }'
```

## Step 4: Make Predictions

### Python Example
```python
import requests

url = "http://localhost:8000/predict"
data = {
    "google_maps_url": "YOUR_GOOGLE_MAPS_URL_HERE"
}

response = requests.post(url, json=data)
result = response.json()

print(f"Prediction: {result['prediction_label']}")
print(f"Confidence: {result['confidence_percentage']}")
```

## Common Issues

### ❌ "Model not found"
**Solution:** Make sure you've trained the model first by running `beer_sales_prediction_2.ipynb`

### ❌ "Port 8000 already in use"
**Solution:** Stop other services on port 8000 or edit `main.py` to use a different port

### ❌ "Module not found"
**Solution:** Make sure virtual environment is activated and dependencies are installed

## What's Next?

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🧪 Run [test_api.py](test_api.py) to verify everything works
- 💡 Check [example_usage.py](example_usage.py) for integration examples
- 📊 Visit http://localhost:8000/docs for interactive API documentation

## Support

For issues or questions, check the main README.md or contact the development team.

---
**Happy Predicting! 🍺**

