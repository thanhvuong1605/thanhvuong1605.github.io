# 🎨 Streamlit Demo Guide

## Overview

A beautiful, interactive web interface for the Beer Sales Prediction API built with Streamlit.

## Features

- ✅ **Easy Input**: Paste Google Maps URLs or use manual input
- ✅ **Real-time Predictions**: Get instant predictions with confidence scores
- ✅ **Rich Analytics**: Visualizations, charts, and detailed feature breakdowns
- ✅ **Interactive Maps**: See location on map
- ✅ **Prediction History**: Track all your predictions
- ✅ **Two Input Modes**: Auto-scrape or manual data entry

## Installation

1. **Install dependencies** (if not already installed):
```bash
pip install -r requirements.txt
```

2. **Make sure the API is running**:
```bash
# In one terminal
cd api_demo
python main.py
```

3. **Start the Streamlit app**:
```bash
# In another terminal
cd api_demo
streamlit run streamlit_demo.py
```

The app will open automatically in your browser at `http://localhost:8501`

## Usage

### Option 1: Auto Scrape Mode

1. Select "Auto Scrape (from URL)" mode
2. Paste a Google Maps URL
3. Click "🔮 Predict"
4. View results with analytics

### Option 2: Manual Input Mode

1. Select "Manual Input" mode
2. Paste Google Maps URL
3. Fill in:
   - Rating (0-5)
   - Number of Reviews
   - Category (Restaurant, Cafe, etc.)
   - Address
4. Click "🔮 Predict"

## What You'll See

### Prediction Results
- **Place Information**: Name, category, address, rating, reviews
- **Prediction**: Beer Seller or Non-Beer Seller
- **Confidence Score**: Percentage with risk level
- **Recommendation**: Actionable advice

### Analytics Dashboard
- **Confidence Gauge**: Visual gauge showing confidence level
- **Features Chart**: Bar chart of key features
- **Detailed Features Table**: All 11+ features used by the model
- **Location Map**: Interactive map showing the place location

### Prediction History
- Track all predictions made in the session
- View timestamp, place name, prediction, and confidence
- Clear history when needed

## Example URLs

Try these sample Google Maps URLs:

```
https://www.google.com/maps/place/Qu%C3%A1n+B%E1%BB%A5i+Garden/@10.8046882,106.7360579,18.45z/data=!4m6!3m5!1s0x317526176671636b:0x471be660ffc59db!8m2!3d10.805121!4d106.735759
```

## Configuration

You can change the API URL in the sidebar if your API is running on a different port or host.

## Troubleshooting

### "Cannot connect to API"
- Make sure the API is running (`python main.py`)
- Check the API URL in the sidebar
- Verify the API is accessible at the specified URL

### "Failed to get prediction result"
- Try using Manual Input mode instead
- Check if the Google Maps URL is valid
- Verify the API logs for errors

### Scraping fails
- Use Manual Input mode for reliable results
- Copy data directly from Google Maps page

## Tips

1. **For best results**: Use Manual Input mode and copy data from Google Maps
2. **Batch predictions**: Use the API directly or make multiple predictions in the Streamlit app
3. **Save results**: Use the prediction history to track multiple locations
4. **API Performance**: The model has 86.76% AUC and 82.62% accuracy

## Next Steps

- Integrate with your business workflow
- Export predictions to CSV/Excel
- Add batch processing for multiple URLs
- Connect to Google Places API for enhanced data

---

**Happy Predicting! 🍺**

