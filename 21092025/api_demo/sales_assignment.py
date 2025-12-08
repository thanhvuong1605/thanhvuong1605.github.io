"""
Sales Assignment Module
Maps place categories and locations to sales territories and sales representatives
"""
import pandas as pd
import h3
from typing import Dict, Optional, List, Tuple
from pathlib import Path


class SalesAssignmentMapper:
    """Maps places to sales territories and representatives"""
    
    def __init__(self, data_dir: str = "../model/sale_assgined"):
        """
        Initialize sales assignment mapper
        
        Args:
            data_dir: Directory containing sales assignment files
        """
        self.data_dir = Path(data_dir)
        self.segment_df = None
        self.assigned_df = None
        self.sales_df = None
        
        self.load_data()
    
    def load_data(self):
        """Load all sales assignment data files"""
        try:
            # Load category to channel mapping
            segment_path = self.data_dir / "segment_new.xlsx"
            if segment_path.exists():
                self.segment_df = pd.read_excel(segment_path)
                print(f"✓ Loaded {len(self.segment_df)} category-channel mappings")
            else:
                print(f"⚠ Warning: {segment_path} not found")
            
            # Load hexagon to channel/territory mapping
            assigned_path = self.data_dir / "Assigned_territory_channel.csv"
            if assigned_path.exists():
                self.assigned_df = pd.read_csv(assigned_path)
                # Drop rows with missing critical data
                self.assigned_df = self.assigned_df.dropna(subset=['HexID', 'Channel', 'Assigned_territory'])
                print(f"✓ Loaded {len(self.assigned_df)} hexagon-channel-territory mappings")
            else:
                print(f"⚠ Warning: {assigned_path} not found")
            
            # Load territory to sales rep mapping
            sales_path = self.data_dir / "salesInfor.xlsx"
            if sales_path.exists():
                self.sales_df = pd.read_excel(sales_path)
                # Filter to only rows with sales rep info
                self.sales_df = self.sales_df[self.sales_df['SRID'].notna()]
                print(f"✓ Loaded {len(self.sales_df)} territory-sales rep mappings")
            else:
                print(f"⚠ Warning: {sales_path} not found")
                
        except Exception as e:
            print(f"✗ Error loading sales assignment data: {str(e)}")
    
    def get_channel_from_category(self, category: str) -> Optional[str]:
        """
        Get sales channel from place category
        
        Args:
            category: Place category (e.g., "Restaurant", "Bar", "Quan Nhau")
            
        Returns:
            Channel name (e.g., "MONT", "TONT", "TOFT") or None
        """
        if self.segment_df is None or not category:
            return None
        
        # Try exact match first
        matches = self.segment_df[self.segment_df['Final_Segment'] == category]
        if len(matches) > 0:
            channel = matches['Channel'].iloc[0]
            if pd.notna(channel) and channel != 'Other':
                return channel
        
        # Try case-insensitive match
        matches = self.segment_df[
            self.segment_df['Final_Segment'].str.lower() == category.lower()
        ]
        if len(matches) > 0:
            channel = matches['Channel'].iloc[0]
            if pd.notna(channel) and channel != 'Other':
                return channel
        
        # Try partial match
        matches = self.segment_df[
            self.segment_df['Final_Segment'].str.contains(category, case=False, na=False)
        ]
        if len(matches) > 0:
            channel = matches['Channel'].iloc[0]
            if pd.notna(channel) and channel != 'Other':
                return channel
        
        return None
    
    def get_territory_from_location(self, hex_id: str, channel: str) -> Tuple[Optional[str], bool]:
        """
        Get assigned territory from hexagon ID and channel
        
        Args:
            hex_id: H3 hexagon ID (should be resolution 8 to match sales data)
            channel: Sales channel (e.g., "MONT", "TONT")
            
        Returns:
            Tuple of (territory name or None, used_parent_hexagon: bool)
            Note: used_parent_hexagon will always be False now since we use resolution 8 directly
        """
        if self.assigned_df is None or not hex_id or not channel:
            return None, False
        
        # Ensure hex_id is string and strip whitespace
        hex_id = str(hex_id).strip() if hex_id else None
        if not hex_id:
            return None, False
        
        # Ensure hex_id is resolution 8 (convert if needed)
        try:
            hex_resolution = h3.get_resolution(hex_id)
            if hex_resolution == 9:
                # Convert to resolution 8
                hex_id = h3.cell_to_parent(hex_id, 8)
            elif hex_resolution != 8:
                # If not resolution 8 or 9, return None
                return None, False
        except:
            return None, False
        
        # Convert HexID column to string for comparison
        assigned_df = self.assigned_df.copy()
        assigned_df['HexID'] = assigned_df['HexID'].astype(str).str.strip()
        
        # Direct match at resolution 8 (no fallback needed)
        matches = assigned_df[
            (assigned_df['HexID'] == hex_id) & 
            (assigned_df['Channel'] == channel)
        ]
        
        if len(matches) > 0:
            territory = matches['Assigned_territory'].iloc[0]
            if pd.notna(territory):
                return territory, False  # Found exact match at resolution 8
        
        return None, False
    
    def get_sales_rep_from_territory(self, territory: str) -> Optional[Dict]:
        """
        Get sales rep information from territory
        
        Args:
            territory: Assigned territory name
            
        Returns:
            Dictionary with SRID, SRNAME, SRHeiwayID or None
        """
        if self.sales_df is None or not territory:
            return None
        
        matches = self.sales_df[self.sales_df['Territory'] == territory]
        
        if len(matches) > 0:
            row = matches.iloc[0]
            return {
                'srid': str(int(row['SRID'])) if pd.notna(row['SRID']) else None,
                'srname': row['SRNAME'] if pd.notna(row['SRNAME']) else None,
                'srheiwayid': row['SRHeiwayID'] if pd.notna(row['SRHeiwayID']) else None
            }
        
        return None
    
    def get_sales_assignment(self, category: str, latitude: float, longitude: float, 
                            hex_id: Optional[str] = None) -> Dict:
        """
        Get complete sales assignment for a place
        
        Args:
            category: Place category
            latitude: Place latitude
            longitude: Place longitude
            hex_id: Optional pre-calculated H3 hexagon ID (will be converted to resolution 8)
            
        Returns:
            Dictionary with channel, territory, and sales rep information
        """
        result = {
            'channel': None,
            'territory': None,
            'sales_rep': None,
            'hex_id': None,
            'used_parent_hexagon': False  # Flag to indicate if parent hexagon lookup was used
        }
        
        # Step 1: Get channel from category
        channel = self.get_channel_from_category(category)
        result['channel'] = channel
        
        if not channel:
            return result
        
        # Step 2: Calculate or use hex_id
        # Sales assignment data uses resolution 8, so calculate at resolution 8 directly
        if not hex_id:
            if latitude and longitude and latitude != 0 and longitude != 0:
                try:
                    # Calculate at resolution 8 to match sales assignment data
                    hex_id = h3.latlng_to_cell(latitude, longitude, 8)
                except:
                    hex_id = None
        else:
            # If hex_id is provided, check if it's resolution 9 and convert to 8
            try:
                hex_resolution = h3.get_resolution(hex_id)
                if hex_resolution == 9:
                    # Convert to parent at resolution 8
                    hex_id = h3.cell_to_parent(hex_id, 8)
                elif hex_resolution != 8:
                    # If not 8 or 9, try to calculate from coordinates
                    if latitude and longitude and latitude != 0 and longitude != 0:
                        hex_id = h3.latlng_to_cell(latitude, longitude, 8)
            except:
                # If conversion fails, try to calculate from coordinates
                if latitude and longitude and latitude != 0 and longitude != 0:
                    try:
                        hex_id = h3.latlng_to_cell(latitude, longitude, 8)
                    except:
                        hex_id = None
        
        result['hex_id'] = hex_id
        
        if not hex_id:
            return result
        
        # Step 3: Get territory from hex_id and channel
        # hex_id is now guaranteed to be resolution 8, so direct lookup (no fallback needed)
        territory, used_parent = self.get_territory_from_location(hex_id, channel)
        result['territory'] = territory
        result['used_parent_hexagon'] = used_parent  # Should always be False now
        
        if not territory:
            return result
        
        # Step 4: Get sales rep from territory
        sales_rep = self.get_sales_rep_from_territory(territory)
        result['sales_rep'] = sales_rep
        
        return result
    
    def get_all_channels_for_location(self, hex_id: str) -> List[Dict]:
        """
        Get all available channels and territories for a location
        
        Args:
            hex_id: H3 hexagon ID (should be resolution 8 to match sales data)
            
        Returns:
            List of dictionaries with channel and territory info
        """
        if self.assigned_df is None or not hex_id:
            return []
        
        # Ensure hex_id is string
        hex_id = str(hex_id).strip() if hex_id else None
        if not hex_id:
            return []
        
        # Ensure hex_id is resolution 8 (convert if needed)
        try:
            hex_resolution = h3.get_resolution(hex_id)
            if hex_resolution == 9:
                # Convert to resolution 8
                hex_id = h3.cell_to_parent(hex_id, 8)
            elif hex_resolution != 8:
                return []
        except:
            return []
        
        # Convert HexID column to string for comparison
        assigned_df = self.assigned_df.copy()
        assigned_df['HexID'] = assigned_df['HexID'].astype(str).str.strip()
        
        # Direct match at resolution 8
        matches = assigned_df[assigned_df['HexID'] == hex_id]
        
        results = []
        for _, row in matches.iterrows():
            channel = row['Channel']
            territory = row['Assigned_territory']
            
            if pd.notna(channel) and pd.notna(territory):
                sales_rep = self.get_sales_rep_from_territory(territory)
                results.append({
                    'channel': channel,
                    'territory': territory,
                    'sales_rep': sales_rep
                })
        
        return results

