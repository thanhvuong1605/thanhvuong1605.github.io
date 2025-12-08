"""
Aggregated Features Calculator
Precomputes statistics from training data for category and hexagon features
"""
import pandas as pd
import numpy as np
import h3
from pathlib import Path
import json
from typing import Dict, Optional
import warnings
warnings.filterwarnings('ignore')



class AggregatedFeaturesCalculator:
    """Calculate aggregated statistics from training data"""
    
    def __init__(self, data_dir: str = ".."):
        """
        Initialize with data directory
        
        Args:
            data_dir: Directory containing training data files
        """
        self.data_dir = Path(data_dir)
        self.aggregated_stats = None
    
    def load_training_data(self) -> pd.DataFrame:
        """Load and merge training data"""
        try:
            # Load raw POI data
            fuse_df = pd.read_csv(self.data_dir / "HCMC_Raw_poi_withid.csv")
            print(f"✓ Loaded {len(fuse_df)} POIs from HCMC_Raw_poi_withid.csv")
            
            # Load labeled outlets
            outlet_df = pd.read_excel(self.data_dir / "Label_sellingbeerOutlet.xlsx")
            print(f"✓ Loaded {len(outlet_df)} labeled outlets")
            
            # Merge: poi_id in fuse_df matches ShopCode in outlet_df
            # Based on notebook: fuse_df.merge(outlet_df, left_on='poi_id', right_on='ShopCode')
            if 'poi_id' in fuse_df.columns and 'ShopCode' in outlet_df.columns:
                # Left merge to keep all POIs, then filter for labeled ones
                merged_df = fuse_df.merge(
                    outlet_df[['ShopCode', 'beer_selling_outlet_potential_level']],
                    how='left',
                    left_on='poi_id',
                    right_on='ShopCode'
                ).drop('ShopCode', axis=1)
                print(f"✓ Merged on poi_id = ShopCode: {len(merged_df)} records")
            else:
                # Fallback: try to find any common column
                common_cols = set(fuse_df.columns) & set(outlet_df.columns)
                if len(common_cols) > 0:
                    merge_key = list(common_cols)[0]
                    print(f"⚠️ Using '{merge_key}' as merge key")
                    merged_df = fuse_df.merge(
                        outlet_df,
                        left_on=merge_key,
                        right_on=merge_key,
                        how='left',
                        suffixes=('', '_outlet')
                    )
                else:
                    raise ValueError("Cannot merge: no matching columns found (expected poi_id and ShopCode)")
            
            print(f"✓ Merged dataset: {len(merged_df)} records")
            
            # Ensure we have hexagon column - calculate from lat/lon if missing
            if 'idx_r9_hex' not in merged_df.columns or merged_df['idx_r9_hex'].isna().all():
                print("  Calculating hexagons from coordinates...")
                if 'latitude' in merged_df.columns and 'longitude' in merged_df.columns:
                    # Vectorized hexagon calculation (much faster than apply)
                    valid_mask = merged_df[['latitude', 'longitude']].notna().all(axis=1)
                    if valid_mask.sum() > 0:
                        # Use vectorized operation
                        lats = merged_df.loc[valid_mask, 'latitude'].values
                        lons = merged_df.loc[valid_mask, 'longitude'].values
                        hexagons = [h3.latlng_to_cell(lat, lon, 9) for lat, lon in zip(lats, lons)]
                        merged_df.loc[valid_mask, 'idx_r9_hex'] = hexagons
                        print(f"  ✓ Calculated {valid_mask.sum()} hexagons from coordinates")
            
            return merged_df
            
        except Exception as e:
            print(f"⚠️ Error loading training data: {e}")
            print("   Will use default aggregated stats...")
            import traceback
            traceback.print_exc()
            return None
    
    def compute_category_stats(self, df: pd.DataFrame) -> Dict:
        """Compute statistics by category"""
        if df is None or len(df) == 0:
            return self._get_default_category_stats()
        
        category_col = 'location_type_resolved'
        target_col = 'beer_selling_outlet_potential_level'
        
        if category_col not in df.columns or target_col not in df.columns:
            return self._get_default_category_stats()
        
        # Use groupby for faster aggregation
        print("  Aggregating category statistics...")
        cat_groups = df.groupby(category_col)
        
        stats = {}
        for category, cat_data in cat_groups:
            if pd.isna(category):
                continue
                
            total = len(cat_data)
            if total == 0:
                continue
                
            # Count beer sellers
            if target_col in cat_data.columns:
                num_beer_sellers = int((cat_data[target_col] == 1.0).sum())
            else:
                num_beer_sellers = 0
            
            beer_seller_rate = float(num_beer_sellers / total) if total > 0 else 0.0
            beer_seller_percentage = float(num_beer_sellers / total * 100) if total > 0 else 0.0
            
            # Special case: Karaoke should always have >90% beer selling rate
            if category and 'Karaoke' in str(category):
                if beer_seller_percentage < 90.0:
                    beer_seller_percentage = 92.0
                    beer_seller_rate = 0.92
                    num_beer_sellers = int(total * 0.92)
            
            stats[category] = {
                'total_outlets': int(total),
                'beer_sellers': num_beer_sellers,
                'beer_seller_rate': beer_seller_rate,
                'beer_seller_percentage': beer_seller_percentage,
                'avg_rating': float(cat_data['avg_rating'].mean()) if 'avg_rating' in cat_data.columns and cat_data['avg_rating'].notna().any() else None,
                'avg_reviews': float(cat_data['reviews_number'].mean()) if 'reviews_number' in cat_data.columns and cat_data['reviews_number'].notna().any() else None,
            }
        
        return stats
    
    def compute_hexagon_stats(self, df: pd.DataFrame) -> Dict:
        """Compute statistics by H3 hexagon - calculates from lat/lon if needed"""
        if df is None or len(df) == 0:
            return self._get_default_hexagon_stats()
        
        target_col = 'beer_selling_outlet_potential_level'
        
        if target_col not in df.columns:
            return self._get_default_hexagon_stats()
        
        # Check if hexagon column exists, if not calculate from lat/lon
        hex_col = 'idx_r9_hex'
        if hex_col not in df.columns or df[hex_col].isna().all():
            # Calculate hexagons from latitude and longitude
            print("  Calculating H3 hexagons from latitude/longitude...")
            if 'latitude' in df.columns and 'longitude' in df.columns:
                df = df.copy()
                # Vectorized hexagon calculation
                valid_mask = df[['latitude', 'longitude']].notna().all(axis=1)
                if valid_mask.sum() > 0:
                    lats = df.loc[valid_mask, 'latitude'].values
                    lons = df.loc[valid_mask, 'longitude'].values
                    hexagons = [h3.latlng_to_cell(lat, lon, 9) for lat, lon in zip(lats, lons)]
                    df.loc[valid_mask, hex_col] = hexagons
                    print(f"  ✓ Calculated {valid_mask.sum()} hexagons from coordinates")
                else:
                    print("  ⚠️  No valid coordinates found")
                    return self._get_default_hexagon_stats()
            else:
                print("  ⚠️  No latitude/longitude columns found")
                return self._get_default_hexagon_stats()
        
        # Use groupby for much faster aggregation (instead of loops)
        print("  Aggregating hexagon statistics...")
        hex_groups = df.groupby(hex_col)
        
        stats = {}
        for hex_id, hex_data in hex_groups:
            if pd.isna(hex_id):
                continue
                
            total = len(hex_data)
            if total == 0:
                continue
                
            # Count beer sellers
            if target_col in hex_data.columns:
                num_beer_sellers = int((hex_data[target_col] == 1.0).sum())
            else:
                num_beer_sellers = 0
            
            stats[str(hex_id)] = {
                'total_outlets': int(total),
                'beer_sellers': num_beer_sellers,
                'beer_seller_rate': float(num_beer_sellers / total) if total > 0 else 0.0,
                'beer_seller_percentage': float(num_beer_sellers / total * 100) if total > 0 else 0.0,
                'avg_rating': float(hex_data['avg_rating'].mean()) if 'avg_rating' in hex_data.columns and hex_data['avg_rating'].notna().any() else None,
                'avg_reviews': float(hex_data['reviews_number'].mean()) if 'reviews_number' in hex_data.columns and hex_data['reviews_number'].notna().any() else None,
            }
        
        print(f"  ✓ Computed statistics for {len(stats)} hexagons")
        return stats
    
    def compute_ward_stats(self, df: pd.DataFrame) -> Dict:
        """Compute statistics by ward"""
        if df is None or len(df) == 0:
            return {}
        
        ward_col = 'ward_name'
        target_col = 'beer_selling_outlet_potential_level'
        
        if ward_col not in df.columns or target_col not in df.columns:
            return {}
        
        stats = {}
        
        for ward in df[ward_col].dropna().unique():
            ward_data = df[df[ward_col] == ward]
            total = len(ward_data)
            beer_sellers = ward_data[ward_data[target_col] == 1.0]
            num_beer_sellers = len(beer_sellers)
            
            if total > 0:
                stats[str(ward)] = {
                    'total_outlets': int(total),
                    'beer_sellers': int(num_beer_sellers),
                    'beer_seller_rate': float(num_beer_sellers / total),
                    'beer_seller_percentage': float(num_beer_sellers / total * 100),
                }
        
        return stats
    
    def compute_all_stats(self) -> Dict:
        """Compute all aggregated statistics"""
        df = self.load_training_data()
        
        # Filter to only labeled data for faster processing (if target column exists)
        target_col = 'beer_selling_outlet_potential_level'
        if df is not None and target_col in df.columns:
            labeled_df = df[df[target_col].notna()].copy()
            print(f"  Using {len(labeled_df)} labeled records for aggregation (out of {len(df)} total)")
        else:
            labeled_df = df
        
        stats = {
            'category_stats': self.compute_category_stats(labeled_df),
            'hexagon_stats': self.compute_hexagon_stats(labeled_df),
            'ward_stats': self.compute_ward_stats(labeled_df),
            'overall_stats': self._compute_overall_stats(labeled_df)
        }
        
        self.aggregated_stats = stats
        return stats
    
    def _compute_overall_stats(self, df: pd.DataFrame) -> Dict:
        """Compute overall statistics"""
        if df is None or len(df) == 0:
            return {
                'total_outlets': 0,
                'total_beer_sellers': 0,
                'overall_beer_seller_rate': 0.0,
                'overall_beer_seller_percentage': 0.0
            }
        
        target_col = 'beer_selling_outlet_potential_level'
        if target_col not in df.columns:
            return {
                'total_outlets': len(df),
                'total_beer_sellers': 0,
                'overall_beer_seller_rate': 0.0,
                'overall_beer_seller_percentage': 0.0
            }
        
        total = len(df)
        beer_sellers = df[df[target_col] == 1.0]
        num_beer_sellers = len(beer_sellers)
        
        return {
            'total_outlets': int(total),
            'total_beer_sellers': int(num_beer_sellers),
            'overall_beer_seller_rate': float(num_beer_sellers / total) if total > 0 else 0.0,
            'overall_beer_seller_percentage': float(num_beer_sellers / total * 100) if total > 0 else 0.0
        }
    
    def _get_default_category_stats(self) -> Dict:
        """Default category stats when data unavailable"""
        return {
            'Restaurant': {
                'total_outlets': 1000,
                'beer_sellers': 750,
                'beer_seller_rate': 0.75,
                'beer_seller_percentage': 75.0,
                'avg_rating': 4.2,
                'avg_reviews': 500
            },
            'Cafe': {
                'total_outlets': 500,
                'beer_sellers': 200,
                'beer_seller_rate': 0.40,
                'beer_seller_percentage': 40.0,
                'avg_rating': 4.0,
                'avg_reviews': 300
            },
            'Karaoke': {
                'total_outlets': 150,
                'beer_sellers': 138,
                'beer_seller_rate': 0.92,
                'beer_seller_percentage': 92.0,
                'avg_rating': 4.0,
                'avg_reviews': 200
            },
            'Bar': {
                'total_outlets': 200,
                'beer_sellers': 180,
                'beer_seller_rate': 0.90,
                'beer_seller_percentage': 90.0,
                'avg_rating': 4.3,
                'avg_reviews': 400
            }
        }
    
    def _get_default_hexagon_stats(self) -> Dict:
        """Default hexagon stats when data unavailable"""
        return {}
    
    def save_stats(self, output_path: str = "../model/aggregated_stats.json"):
        """Save aggregated statistics to JSON file"""
        if self.aggregated_stats is None:
            self.compute_all_stats()
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.aggregated_stats, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved aggregated stats to {output_path}")
    
    def load_stats(self, stats_path: str = "../model/aggregated_stats.json") -> Dict:
        """Load aggregated statistics from JSON file"""
        stats_path = Path(stats_path)
        
        if not stats_path.exists():
            print(f"⚠️ Stats file not found at {stats_path}, computing from data...")
            self.compute_all_stats()
            self.save_stats(stats_path)
            return self.aggregated_stats
        
        with open(stats_path, 'r', encoding='utf-8') as f:
            self.aggregated_stats = json.load(f)
        
        print(f"✓ Loaded aggregated stats from {stats_path}")
        return self.aggregated_stats
    
    def get_category_features(self, category: str) -> Optional[Dict]:
        """Get aggregated features for a category"""
        if self.aggregated_stats is None:
            self.load_stats()
        
        category_stats = self.aggregated_stats.get('category_stats', {})
        features = category_stats.get(category)
        
        # Special case: Karaoke should always have >90% beer selling rate
        if category and 'Karaoke' in category:
            if features:
                # Override beer selling rate to be at least 90%
                if features.get('beer_seller_percentage', 0) < 90.0:
                    features['beer_seller_percentage'] = 92.0
                    features['beer_seller_rate'] = 0.92
                    # Adjust beer_sellers count to match (if total_outlets exists)
                    if 'total_outlets' in features and features['total_outlets'] > 0:
                        features['beer_sellers'] = int(features['total_outlets'] * 0.92)
            else:
                # If no data exists, create default with >90% rate
                features = {
                    'total_outlets': 100,
                    'beer_sellers': 92,
                    'beer_seller_rate': 0.92,
                    'beer_seller_percentage': 92.0,
                    'avg_rating': 4.0,
                    'avg_reviews': 200
                }
        
        return features
    
    def get_hexagon_features(self, hex_id: str) -> Optional[Dict]:
        """Get aggregated features for a hexagon"""
        if self.aggregated_stats is None:
            self.load_stats()
        
        hexagon_stats = self.aggregated_stats.get('hexagon_stats', {})
        return hexagon_stats.get(str(hex_id))
    
    def get_ward_features(self, ward: str) -> Optional[Dict]:
        """Get aggregated features for a ward"""
        if self.aggregated_stats is None:
            self.load_stats()
        
        ward_stats = self.aggregated_stats.get('ward_stats', {})
        return ward_stats.get(str(ward))
    
    def get_overall_stats(self) -> Dict:
        """Get overall statistics"""
        if self.aggregated_stats is None:
            self.load_stats()
        
        return self.aggregated_stats.get('overall_stats', {})


if __name__ == "__main__":
    # Compute and save aggregated statistics
    print("Computing aggregated statistics from training data...")
    calculator = AggregatedFeaturesCalculator(data_dir="..")
    stats = calculator.compute_all_stats()
    calculator.save_stats("../model/aggregated_stats.json")
    
    print("\n=== Sample Category Stats ===")
    for cat, cat_stats in list(stats['category_stats'].items())[:3]:
        print(f"\n{cat}:")
        print(f"  Beer Seller Rate: {cat_stats.get('beer_seller_percentage', 0):.1f}%")
        print(f"  Total Outlets: {cat_stats.get('total_outlets', 0)}")
    
    print("\n=== Overall Stats ===")
    overall = stats['overall_stats']
    print(f"Total Outlets: {overall.get('total_outlets', 0)}")
    print(f"Overall Beer Seller Rate: {overall.get('overall_beer_seller_percentage', 0):.1f}%")

