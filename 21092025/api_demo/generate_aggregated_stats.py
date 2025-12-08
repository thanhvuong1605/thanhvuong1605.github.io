"""
Script to generate aggregated statistics from training data
Run this script to precompute category and hexagon statistics
"""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from aggregated_features import AggregatedFeaturesCalculator

if __name__ == "__main__":
    print("=" * 60)
    print("Generating Aggregated Statistics from Training Data")
    print("=" * 60)
    
    # Initialize calculator
    calculator = AggregatedFeaturesCalculator(data_dir="..")
    
    # Compute all statistics
    print("\n📊 Computing statistics...")
    stats = calculator.compute_all_stats()
    
    # Save to model directory
    output_path = "../model/aggregated_stats.json"
    calculator.save_stats(output_path)
    
    print("\n" + "=" * 60)
    print("✅ Aggregated statistics generated successfully!")
    print("=" * 60)
    
    # Print summary
    print("\n📈 Summary:")
    print(f"  - Categories analyzed: {len(stats.get('category_stats', {}))}")
    print(f"  - Hexagons analyzed: {len(stats.get('hexagon_stats', {}))}")
    print(f"  - Wards analyzed: {len(stats.get('ward_stats', {}))}")
    
    overall = stats.get('overall_stats', {})
    print(f"\n  Overall Statistics:")
    print(f"    - Total Outlets: {overall.get('total_outlets', 0):,}")
    print(f"    - Beer Sellers: {overall.get('total_beer_sellers', 0):,}")
    print(f"    - Beer Seller Rate: {overall.get('overall_beer_seller_percentage', 0):.1f}%")
    
    print(f"\n💾 Saved to: {output_path}")
    print("\n✨ You can now use these statistics in the API!")

