# Aggregated Features Guide

## Overview

The API now includes **precomputed aggregated statistics** from training data that provide context about:
- **Category-level statistics**: Beer seller rates, distributions per business category
- **Hexagon-level statistics**: Beer seller rates per H3 hexagon area
- **Ward-level statistics**: Beer seller rates per ward/district
- **Overall statistics**: Overall beer seller rates from training data

## How It Works

### 1. Generate Aggregated Statistics

First, run the script to compute statistics from training data:

```bash
cd api_demo
python generate_aggregated_stats.py
```

This will:
- Load training data from `../HCMC_Raw_poi_withid.csv` and `../Label_sellingbeerOutlet.xlsx`
- Compute statistics by category, hexagon, and ward
- Save to `../model/aggregated_stats.json`

### 2. API Integration

The aggregated features are automatically included in API responses:

```json
{
  "success": true,
  "prediction": 1,
  "aggregated_features": {
    "category_features": {
      "beer_seller_rate": 0.75,
      "beer_seller_percentage": 75.0,
      "total_outlets": 1000,
      "beer_sellers": 750,
      "avg_rating": 4.2,
      "avg_reviews": 500
    },
    "hexagon_features": {
      "beer_seller_rate": 0.60,
      "beer_seller_percentage": 60.0,
      "total_outlets": 50,
      "beer_sellers": 30
    },
    "ward_features": {
      "beer_seller_rate": 0.55,
      "beer_seller_percentage": 55.0,
      "total_outlets": 200,
      "beer_sellers": 110
    },
    "overall_stats": {
      "overall_beer_seller_rate": 0.50,
      "overall_beer_seller_percentage": 50.0,
      "total_outlets": 10000,
      "total_beer_sellers": 5000
    }
  }
}
```

### 3. Frontend Display

The Streamlit frontend automatically displays:

#### Category Statistics
- Beer seller rate for the location's category
- Total outlets in that category
- Distribution chart (beer sellers vs non-beer sellers)
- Average rating for the category

#### Hexagon Statistics
- Beer seller rate in that hexagon area (~0.46 km²)
- Total outlets in the hexagon
- Comparison chart vs overall average

#### Ward Statistics
- Beer seller rate in that ward
- Total outlets in the ward

#### Overall Statistics
- Overall beer seller rate from training data
- Total outlets and beer sellers in training set

## Features Computed

### Category Features
- `beer_seller_rate`: Proportion of outlets in this category that sell beer
- `beer_seller_percentage`: Percentage (0-100)
- `total_outlets`: Total number of outlets in this category
- `beer_sellers`: Number of beer-selling outlets
- `avg_rating`: Average rating for outlets in this category
- `avg_reviews`: Average number of reviews

### Hexagon Features
- `beer_seller_rate`: Proportion of outlets in this hexagon that sell beer
- `beer_seller_percentage`: Percentage (0-100)
- `total_outlets`: Total number of outlets in this hexagon
- `beer_sellers`: Number of beer-selling outlets
- `avg_rating`: Average rating for outlets in this hexagon
- `avg_reviews`: Average number of reviews

### Ward Features
- `beer_seller_rate`: Proportion of outlets in this ward that sell beer
- `beer_seller_percentage`: Percentage (0-100)
- `total_outlets`: Total number of outlets in this ward
- `beer_sellers`: Number of beer-selling outlets

## Usage Example

```python
from aggregated_features import AggregatedFeaturesCalculator

# Initialize calculator
calculator = AggregatedFeaturesCalculator(data_dir="..")

# Load precomputed stats
stats = calculator.load_stats("../model/aggregated_stats.json")

# Get category features
category_features = calculator.get_category_features("Restaurant")
print(f"Restaurant beer seller rate: {category_features['beer_seller_percentage']:.1f}%")

# Get hexagon features
hex_features = calculator.get_hexagon_features("8965b566ad7ffff")
print(f"Hexagon beer seller rate: {hex_features['beer_seller_percentage']:.1f}%")
```

## Benefits

1. **Context**: Understand how a location compares to similar locations
2. **Validation**: See if prediction aligns with historical patterns
3. **Insights**: Identify high-potential areas and categories
4. **Transparency**: Show data-driven reasoning behind predictions

## Troubleshooting

### Stats file not found
If `aggregated_stats.json` doesn't exist, the API will:
- Try to compute from training data automatically
- Fall back to default statistics if data unavailable
- Continue working without aggregated features

### Missing category/hexagon
If a category or hexagon isn't in training data:
- Aggregated features will be `None` for that location
- API will still make predictions using other features
- Frontend will show available statistics only

### Data loading errors
If training data can't be loaded:
- Check file paths are correct
- Verify CSV/Excel files exist
- Check column names match expected format
- Default statistics will be used

## Next Steps

- Add more aggregated features (e.g., by province, by rating range)
- Include time-based statistics (trends over time)
- Add confidence intervals for statistics
- Visualize hexagon boundaries on map

