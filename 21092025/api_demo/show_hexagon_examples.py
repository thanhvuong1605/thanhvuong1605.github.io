"""
Script to show examples of hexagons that have data in aggregated statistics
"""
import json
from pathlib import Path
from aggregated_features import AggregatedFeaturesCalculator

def show_hexagon_examples():
    """Show examples of hexagons with data"""
    
    # Initialize calculator
    calculator = AggregatedFeaturesCalculator(data_dir="..")
    
    # Try to load existing stats
    stats_path = Path("../model/aggregated_stats.json")
    if stats_path.exists():
        print("📊 Loading existing aggregated statistics...")
        stats = calculator.load_stats(str(stats_path))
    else:
        print("📊 Computing aggregated statistics from training data...")
        stats = calculator.compute_all_stats()
        calculator.save_stats(str(stats_path))
    
    # Show hexagon examples
    hexagon_stats = stats.get('hexagon_stats', {})
    
    if not hexagon_stats:
        print("\n⚠️ No hexagon statistics found in aggregated data.")
        print("This might mean:")
        print("  - Training data doesn't have hexagon information")
        print("  - Hexagon column name might be different")
        print("  - Need to regenerate aggregated stats")
        return
    
    print(f"\n✅ Found {len(hexagon_stats)} hexagons with data")
    print("\n" + "="*80)
    print("📋 Examples of Hexagons with Data:")
    print("="*80)
    
    # Show first 10 examples
    examples = list(hexagon_stats.items())[:10]
    
    for i, (hex_id, hex_data) in enumerate(examples, 1):
        print(f"\n{i}. Hexagon: {hex_id}")
        print(f"   - Total Outlets: {hex_data.get('total_outlets', 0):,}")
        print(f"   - Beer Sellers: {hex_data.get('beer_sellers', 0):,}")
        print(f"   - Beer Seller Rate: {hex_data.get('beer_seller_percentage', 0):.1f}%")
        if hex_data.get('avg_rating'):
            print(f"   - Average Rating: {hex_data.get('avg_rating', 0):.2f} ⭐")
        if hex_data.get('avg_reviews'):
            print(f"   - Average Reviews: {hex_data.get('avg_reviews', 0):.0f}")
    
    # Show hexagons with highest beer seller rates
    print("\n" + "="*80)
    print("🏆 Top 5 Hexagons by Beer Seller Rate:")
    print("="*80)
    
    sorted_hexagons = sorted(
        hexagon_stats.items(),
        key=lambda x: x[1].get('beer_seller_percentage', 0),
        reverse=True
    )[:5]
    
    for i, (hex_id, hex_data) in enumerate(sorted_hexagons, 1):
        print(f"\n{i}. Hexagon: {hex_id}")
        print(f"   - Beer Seller Rate: {hex_data.get('beer_seller_percentage', 0):.1f}%")
        print(f"   - Total Outlets: {hex_data.get('total_outlets', 0):,}")
        print(f"   - Beer Sellers: {hex_data.get('beer_sellers', 0):,}")
    
    # Show hexagons with most outlets
    print("\n" + "="*80)
    print("📈 Top 5 Hexagons by Number of Outlets:")
    print("="*80)
    
    sorted_by_outlets = sorted(
        hexagon_stats.items(),
        key=lambda x: x[1].get('total_outlets', 0),
        reverse=True
    )[:5]
    
    for i, (hex_id, hex_data) in enumerate(sorted_by_outlets, 1):
        print(f"\n{i}. Hexagon: {hex_id}")
        print(f"   - Total Outlets: {hex_data.get('total_outlets', 0):,}")
        print(f"   - Beer Sellers: {hex_data.get('beer_sellers', 0):,}")
        print(f"   - Beer Seller Rate: {hex_data.get('beer_seller_percentage', 0):.1f}%")
    
    # Show sample hexagon IDs for testing
    print("\n" + "="*80)
    print("🧪 Sample Hexagon IDs for Testing:")
    print("="*80)
    print("\nYou can use these hexagon IDs - find Google Maps URLs near these locations:")
    
    sample_hexagons = list(hexagon_stats.items())[:5]
    for hex_id, hex_data in sample_hexagons:
        print(f"\n  - Hexagon: {hex_id}")
        print(f"    Outlets: {hex_data.get('total_outlets', 0)}, Beer Sellers: {hex_data.get('beer_sellers', 0)}")
        print(f"    Rate: {hex_data.get('beer_seller_percentage', 0):.1f}%")
    
    # Also show known examples from training data
    print("\n" + "="*80)
    print("📍 Known Hexagon Examples from Training Data:")
    print("="*80)
    known_hexagons = [
        ("8965b56711bffff", "10.806100, 106.714103", "5 outlets"),
        ("8965b5642a7ffff", "10.832930, 106.671870", "4 outlets"),
        ("8965b56708fffff", "10.804121, 106.735546", "4 outlets"),
        ("8965b56634bffff", "10.786660, 106.689389", "4 outlets"),
        ("8965b5643c7ffff", "10.805121, 106.735759", "Example from docs"),
    ]
    
    for hex_id, coords, info in known_hexagons:
        lat, lon = coords.split(", ")
        print(f"\n  - Hexagon: {hex_id}")
        print(f"    Location: {coords}")
        print(f"    Info: {info}")
        print(f"    Google Maps: https://www.google.com/maps?q={lat},{lon}")
        # Check if this hexagon has stats
        if hex_id in hexagon_stats:
            hex_data = hexagon_stats[hex_id]
            print(f"    ✓ Has aggregated stats: {hex_data.get('beer_seller_percentage', 0):.1f}% beer seller rate")
        else:
            print(f"    ⚠️  Not in aggregated stats (may need to regenerate)")
    
    print("\n" + "="*80)
    print("💡 To use in API:")
    print("="*80)
    print("""
    1. Use any Google Maps URL near the coordinates above
    2. The API will automatically calculate the hexagon from coordinates
    3. If the hexagon is in training data, you'll see aggregated statistics
    
    Example:
    - Find a restaurant near 10.804121, 106.735546
    - Use its Google Maps URL in the API
    - The hexagon 8965b56708fffff will be calculated and stats shown
    """)

if __name__ == "__main__":
    show_hexagon_examples()

