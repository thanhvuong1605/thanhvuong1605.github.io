# H3 Hexagon Examples with Data

## Example Hexagons from Training Data

Here are real hexagon IDs from the training data that you can use for testing:

### Top Hexagons by Number of Outlets

1. **Hexagon: `8965b56711bffff`**
   - Outlets: 5
   - Sample Location: 10.806100, 106.714103
   - [View on Google Maps](https://www.google.com/maps?q=10.8060997,106.7141027)

2. **Hexagon: `8965b5642a7ffff`**
   - Outlets: 4
   - Sample Location: 10.832930, 106.671870
   - [View on Google Maps](https://www.google.com/maps?q=10.8329295,106.6718702)

3. **Hexagon: `8965b56708fffff`**
   - Outlets: 4
   - Sample Location: 10.804121, 106.735546
   - [View on Google Maps](https://www.google.com/maps?q=10.8041213,106.7355456)

4. **Hexagon: `8965b56634bffff`**
   - Outlets: 4
   - Sample Location: 10.786660, 106.689389
   - [View on Google Maps](https://www.google.com/maps?q=10.78666,106.689389)

5. **Hexagon: `8965b566417ffff`**
   - Outlets: 4
   - Sample Location: 10.738602, 106.713501
   - [View on Google Maps](https://www.google.com/maps?q=10.7386017,106.7135009)

### Example from Documentation

- **Hexagon: `8965b5643c7ffff`** (from FEATURES.md)
  - Used in example: Quán Bụi Garden
  - Location: ~10.805121, 106.735759

## How to Use These Hexagons

### Option 1: Use Google Maps URLs Near These Locations

1. Click on any of the Google Maps links above
2. Find a restaurant/cafe/bar in that area
3. Copy the Google Maps URL
4. Use it in the Streamlit demo or API

### Option 2: Test with Specific Coordinates

You can test the API with coordinates that fall within these hexagons:

```python
# Example: Test with hexagon 8965b56708fffff
test_url = "https://www.google.com/maps/place/Test/@10.804121,106.735546"
```

### Option 3: Check Hexagon Statistics

Run the script to see all hexagons with data:

```bash
cd api_demo
python show_hexagon_examples.py
```

## Understanding H3 Hexagons

- **Resolution 9** (`idx_r9_hex`): Each hexagon covers ~0.46 km²
- **Area**: About 2-3 city blocks in Ho Chi Minh City
- **Purpose**: Identifies commercial districts and areas with high beer sales concentration

## Regenerating Aggregated Stats

If hexagon statistics are missing, regenerate them:

```bash
cd api_demo
python generate_aggregated_stats.py
```

This will compute statistics for all hexagons in the training data.

