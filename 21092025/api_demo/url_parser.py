"""
Utility functions to parse Google Maps URLs and extract POI information
"""
import re
from urllib.parse import unquote, urlparse, parse_qs
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional


def parse_google_maps_url(url: str) -> Dict[str, any]:
    """
    Parse Google Maps URL to extract place information
    
    Args:
        url: Google Maps URL
        
    Returns:
        Dictionary containing place_name, latitude, longitude, place_id
    """
    result = {
        'place_name': None,
        'latitude': None,
        'longitude': None,
        'place_id': None,
        'address': None
    }
    
    # Extract place name from URL path
    # Pattern: /maps/place/Place+Name/@lat,lon
    place_pattern = r'/place/([^/@]+)'
    place_match = re.search(place_pattern, url)
    if place_match:
        result['place_name'] = unquote(place_match.group(1)).replace('+', ' ')
    
    # Extract coordinates from URL
    # Pattern: @lat,lon,zoom or @lat,lon
    coord_pattern = r'@(-?\d+\.\d+),(-?\d+\.\d+)'
    coord_match = re.search(coord_pattern, url)
    if coord_match:
        result['latitude'] = float(coord_match.group(1))
        result['longitude'] = float(coord_match.group(2))
    
    # Extract place_id if available
    place_id_pattern = r'0x[0-9a-f]+:0x[0-9a-f]+'
    place_id_match = re.search(place_id_pattern, url)
    if place_id_match:
        result['place_id'] = place_id_match.group(0)
    
    return result


def scrape_place_details_from_google(url: str) -> Dict[str, any]:
    """
    Scrape place details from Google Maps URL
    
    Args:
        url: Google Maps URL
        
    Returns:
        Dictionary with place details including rating, reviews, category
    """
    basic_info = parse_google_maps_url(url)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        page_text = response.text
        
        # Debug: Save HTML for inspection (optional)
        # with open('/tmp/google_maps_debug.html', 'w', encoding='utf-8') as f:
        #     f.write(page_text)
        #     print("Debug: Saved HTML to /tmp/google_maps_debug.html")
        
        # === EXTRACT FROM GOOGLE MAPS EMBEDDED DATA ===
        # Google Maps embeds data in window.APP_INITIALIZATION_STATE or window.APP_OPTIONS
        # Try to extract from these JavaScript variables
        app_data_patterns = [
            r'window\.APP_INITIALIZATION_STATE\s*=\s*(\[.+?\]);',
            r'window\.APP_OPTIONS\s*=\s*(\{.+?\});',
            r'"APP_INITIALIZATION_STATE":\s*(\[.+?\])',
        ]
        
        embedded_data = None
        for pattern in app_data_patterns:
            match = re.search(pattern, page_text, re.DOTALL)
            if match:
                try:
                    import json
                    embedded_data = json.loads(match.group(1))
                    print(f"✓ Found embedded Google Maps data")
                    break
                except:
                    continue
        
        # === EXTRACT RATING ===
        rating = None
        # Pattern 1: Look for rating in various formats
        rating_patterns = [
            r'"aggregateRating":\s*{\s*"ratingValue":\s*([0-9.]+)',
            r'"rating":\s*([0-9.]+)',
            r'"ratingValue":\s*"([0-9.]+)"',
            r'\["[^"]*",\s*null,\s*\[\s*([0-9.]+)',  # Array format
        ]
        for pattern in rating_patterns:
            match = re.search(pattern, page_text)
            if match:
                try:
                    rating = float(match.group(1))
                    break
                except:
                    continue
        
        # === EXTRACT REVIEWS COUNT ===
        reviews = 0
        reviews_patterns = [
            r'"aggregateRating":\s*{[^}]*"reviewCount":\s*([0-9,]+)',
            r'"userRatingCount":\s*([0-9,]+)',
            r'"reviewCount":\s*"([0-9,]+)"',
            r'\["[^"]*",\s*null,\s*\[[0-9.]+,\s*([0-9,]+)',  # Array format
            r'(\d{1,3}(?:,\d{3})*)\s*reviews',
        ]
        for pattern in reviews_patterns:
            match = re.search(pattern, page_text)
            if match:
                try:
                    reviews_str = match.group(1).replace(',', '')
                    reviews = int(reviews_str)
                    break
                except:
                    continue
        
        # === EXTRACT CATEGORY ===
        category = None
        
        # Method 1: Try to extract from embedded JSON data (most reliable)
        if embedded_data:
            try:
                # Recursively search for category in embedded data
                def find_category_in_data(obj, path=""):
                    if isinstance(obj, dict):
                        # Check common category keys
                        for key in ['category', 'type', '@type', 'businessType', 'placeType', 'primaryType']:
                            if key in obj:
                                val = obj[key]
                                if isinstance(val, str) and len(val) < 100:
                                    # Normalize common patterns
                                    val_lower = val.lower()
                                    if 'coffee' in val_lower or 'cafe' in val_lower or 'cà phê' in val_lower:
                                        return 'Cafe'
                                    elif 'restaurant' in val_lower or 'nhà hàng' in val_lower:
                                        return 'Restaurant'
                                    elif 'bar' in val_lower:
                                        return 'Bar'
                                    elif 'karaoke' in val_lower:
                                        return 'Karaoke'
                                    return val
                        # Recursively search nested objects
                        for v in obj.values():
                            result = find_category_in_data(v, path + "." + str(type(v)))
                            if result:
                                return result
                    elif isinstance(obj, list):
                        for item in obj:
                            result = find_category_in_data(item, path)
                            if result:
                                return result
                    return None
                
                category = find_category_in_data(embedded_data)
                if category:
                    print(f"✓ Found category in embedded data: {category}")
            except Exception as e:
                print(f"⚠️ Error parsing embedded data for category: {e}")
        
        # Method 2: Look for structured data patterns (JSON-LD, Schema.org)
        if not category:
            category_patterns = [
                # Schema.org patterns
                r'"@type":\s*"([^"]*(?:Cafe|Coffee|CoffeeShop|Restaurant|Bar|Karaoke)[^"]*)"',
                r'"type":\s*"([^"]*(?:cafe|coffee|restaurant|bar|karaoke)[^"]*)"',
                r'"category":\s*"([^"]+)"',
                r'"businessType":\s*"([^"]+)"',
                r'"placeType":\s*"([^"]+)"',
                r'"primaryType":\s*"([^"]+)"',
                # Array patterns
                r'\["([^"]*(?:Coffee shop|Coffee|Cafe|Restaurant|Bar|Karaoke)[^"]*)",',
                r'\["([^"]*(?:coffee|cafe|restaurant|bar|karaoke)[^"]*)",',
            ]
            for pattern in category_patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    category = match.group(1)
                    # Clean up category
                    category = category.replace('Schema/', '').replace('Organization/', '')
                    # Normalize common variations
                    category_lower = category.lower()
                    if 'coffee' in category_lower or 'cafe' in category_lower or 'cà phê' in category_lower or 'coffee shop' in category_lower:
                        category = 'Cafe'
                    elif 'restaurant' in category_lower or 'nhà hàng' in category_lower:
                        category = 'Restaurant'
                    elif 'bar' in category_lower or 'pub' in category_lower:
                        category = 'Bar'
                    elif 'karaoke' in category_lower:
                        category = 'Karaoke'
                    if category:
                        print(f"✓ Found category from pattern: {category}")
                        break
        
        # Method 3: Look for category text near the place name (e.g., "4.1 (1,477) · Coffee shop")
        if not category and basic_info.get('place_name'):
            # Pattern 1: Look for "Coffee shop" or similar patterns directly in text
            # Google Maps often displays: "Coffee shop" or "Restaurant" as plain text
            direct_category_patterns = [
                r'(?:^|[\s>])(Coffee\s+shop|Coffee\s+store|Café|Cafe|Restaurant|Bar|Karaoke)(?:[\s<,\.]|$)',
                r'["\'](Coffee\s+shop|Coffee\s+store|Café|Cafe|Restaurant|Bar|Karaoke)["\']',
            ]
            for pattern in direct_category_patterns:
                matches = re.finditer(pattern, page_text, re.IGNORECASE)
                for match in matches:
                    potential_cat = match.group(1).strip()
                    cat_lower = potential_cat.lower()
                    if 'coffee' in cat_lower or 'cafe' in cat_lower or 'café' in cat_lower:
                        category = 'Cafe'
                        print(f"✓ Found category from direct text: {category}")
                        break
                    elif 'restaurant' in cat_lower:
                        category = 'Restaurant'
                        print(f"✓ Found category from direct text: {category}")
                        break
                    elif 'bar' in cat_lower:
                        category = 'Bar'
                        print(f"✓ Found category from direct text: {category}")
                        break
                if category:
                    break
            
            # Pattern 2: Rating · Category pattern
            # Example: "4.1" or "4.1 ★" followed by reviews, then "·" then category
            if not category:
                rating_category_pattern = r'(?:\d+\.?\d*\s*(?:★|stars?)?\s*\([^)]+\)\s*)?·\s*([^·\n<>]+?)(?:\s*·|$|<|\n)'
                matches = re.finditer(rating_category_pattern, page_text, re.IGNORECASE)
                for match in matches:
                    potential_cat = match.group(1).strip()
                    # Filter out common non-category text
                    if (len(potential_cat) < 50 and 
                        len(potential_cat) > 2 and
                        not any(x in potential_cat.lower() for x in ['http', 'www', '.com', 'km', 'mi', 'reviews', 'rating', 'star'])):
                        # Check if it looks like a category
                        cat_lower = potential_cat.lower()
                        if any(word in cat_lower for word in ['coffee', 'cafe', 'restaurant', 'bar', 'pub', 'karaoke', 'shop', 'store', 'nhà hàng', 'quán']):
                            # Normalize
                            if 'coffee' in cat_lower or 'cafe' in cat_lower or 'cà phê' in cat_lower or 'coffee shop' in cat_lower:
                                category = 'Cafe'
                            elif 'restaurant' in cat_lower or 'nhà hàng' in cat_lower:
                                category = 'Restaurant'
                            elif 'bar' in cat_lower or 'pub' in cat_lower:
                                category = 'Bar'
                            elif 'karaoke' in cat_lower:
                                category = 'Karaoke'
                            if category:
                                print(f"✓ Found category near rating: {category}")
                                break
            
            # Pattern 3: Place name followed by category
            if not category:
                name_escaped = re.escape(basic_info['place_name'])
                pattern = name_escaped + r'[^·]*·\s*([^·\n<>]+?)(?:\s*·|$|<)'
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    potential_cat = match.group(1).strip()
                    if (len(potential_cat) < 50 and 
                        not any(x in potential_cat.lower() for x in ['http', 'www', '.com'])):
                        cat_lower = potential_cat.lower()
                        if any(word in cat_lower for word in ['coffee', 'cafe', 'restaurant', 'bar', 'pub', 'karaoke', 'shop', 'store']):
                            # Normalize
                            if 'coffee' in cat_lower or 'cafe' in cat_lower or 'cà phê' in cat_lower or 'coffee shop' in cat_lower:
                                category = 'Cafe'
                            elif 'restaurant' in cat_lower or 'nhà hàng' in cat_lower:
                                category = 'Restaurant'
                            elif 'bar' in cat_lower or 'pub' in cat_lower:
                                category = 'Bar'
                            elif 'karaoke' in cat_lower:
                                category = 'Karaoke'
                            if category:
                                print(f"✓ Found category near place name: {category}")
        
        # Debug: If still no category found
        if not category:
            print(f"⚠️ Could not extract category from Google Maps page")
        
        # === EXTRACT ADDRESS ===
        address = None
        address_patterns = [
            r'"address":\s*"([^"]+)"',
            r'"streetAddress":\s*"([^"]+)"',
            r'\["([^"]*\d+[^"]*(?:Thành phố|Quận|Huyện)[^"]*)"',
            r'address.*?:\s*"([^"]+Hồ Chí Minh[^"]*)"',
        ]
        for pattern in address_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                address = match.group(1)
                # Clean up address
                address = address.replace('\\u0027', "'").replace('\\/', '/')
                break
        
        # Calculate derived features for temporal data
        # Since we can't get historical data, estimate based on current values
        last_avg_rating = rating if rating else None
        last_1_reviews_number = reviews * 0.3 if reviews else 0  # Assume 30% of reviews in recent period
        last_2_reviews_number = reviews * 0.5 if reviews else 0  # Assume 50% of reviews in last 2 periods
        
        basic_info.update({
            'avg_rating': rating,
            'reviews_number': reviews,
            'last_avg_rating': last_avg_rating,
            'last_1_reviews_number': last_1_reviews_number,
            'last_2_reviews_number': last_2_reviews_number,
            'category': category,
            'address': address
        })
        
    except Exception as e:
        print(f"Error scraping URL: {e}")
        # Set defaults if scraping fails
        basic_info['avg_rating'] = None
        basic_info['reviews_number'] = 0
        basic_info['last_avg_rating'] = None
        basic_info['last_1_reviews_number'] = 0
        basic_info['last_2_reviews_number'] = 0
        basic_info['category'] = None
    
    return basic_info


def extract_ward_from_address(address: str) -> str:
    """Extract ward name from address - handles multiple Vietnamese address patterns"""
    if not address:
        return None
    
    # Pattern 1: "Phường X" (e.g., Phường 10, Phường Bến Nghé)
    ward_pattern_phuong = r'Phường\s+([^,]+)'
    match = re.search(ward_pattern_phuong, address, re.IGNORECASE)
    if match:
        return f"Phường {match.group(1).strip()}"
    
    # Pattern 2: Ward name before district (e.g., "Thảo Điền, Thủ Đức" or "Bến Nghé, Quận 1")
    # Common pattern: "street, WARD, DISTRICT, PROVINCE"
    parts = [p.strip() for p in address.split(',')]
    if len(parts) >= 3:
        # The second-to-last or third-to-last part is often the ward
        for i in range(1, min(4, len(parts))):
            potential_ward = parts[i].strip()
            # Check if it looks like a ward (not a district or province)
            if not any(keyword in potential_ward for keyword in ['Quận', 'Huyện', 'Thành phố', 'Tỉnh', 'TP', 'District']):
                # Check if next part is a district
                if i + 1 < len(parts):
                    next_part = parts[i + 1].strip()
                    if any(keyword in next_part for keyword in ['Quận', 'Huyện', 'Thủ Đức', 'District']):
                        # This is likely a ward
                        return potential_ward
    
    # Pattern 3: Look for common ward names in HCMC
    common_wards = [
        'Thảo Điền', 'An Phú', 'Bình Trưng Đông', 'Bình Trưng Tây',
        'Bến Nghé', 'Đa Kao', 'Tân Định', 'Cô Giang',
        'An Khánh', 'An Lợi Đông', 'Bình An', 'Bình Khánh',
        'Cát Lái', 'Thạnh Mỹ Lợi', 'Thủ Thiêm'
    ]
    for ward in common_wards:
        if ward in address:
            return ward
    
    return None


def extract_province_from_address(address: str) -> str:
    """Extract province name from address"""
    if not address:
        return 'Thành phố Hồ Chí Minh'  # Default to HCMC
    
    # Look for common province patterns
    province_patterns = [
        r'Thành phố Hồ Chí Minh',
        r'Hồ Chí Minh',
        r'TP\.?\s*HCM',
        r'TP\.\s*Hồ Chí Minh',
        r'Sài Gòn'
    ]
    
    for pattern in province_patterns:
        if re.search(pattern, address, re.IGNORECASE):
            return 'Thành phố Hồ Chí Minh'
    
    # Try to extract province name from the end of address
    # Vietnamese addresses typically end with province name
    parts = address.split(',')
    if len(parts) > 0:
        last_part = parts[-1].strip()
        # Check if it looks like a province
        if any(word in last_part for word in ['Thành phố', 'Tỉnh', 'TP']):
            return last_part
    
    return 'Thành phố Hồ Chí Minh'  # Default


def infer_category_from_name(name: str, scraped_category: Optional[str] = None) -> str:
    """
    Infer location category from place name or scraped category
    Maps to categories similar to those in training data
    """
    if scraped_category:
        return scraped_category
    
    if not name:
        return 'Restaurant'
    
    name_lower = name.lower()
    
    # IMPORTANT: Check coffee shop keywords FIRST (more specific)
    # Vietnamese coffee shops often have "phê" in the name (from "Cà Phê" = Coffee)
    if any(word in name_lower for word in ['cafe', 'cà phê', 'coffee', 'caphe', 'phê', 'café']):
        return 'Cafe'
    elif any(word in name_lower for word in ['bar', 'pub', 'beer', 'bia']):
        return 'Bar'
    elif any(word in name_lower for word in ['karaoke']):
        return 'Karaoke'
    elif any(word in name_lower for word in ['lẩu', 'hotpot', 'hot pot']):
        return 'Hot pot restaurant'
    # Then check restaurant keywords
    elif any(word in name_lower for word in ['nhà hàng', 'restaurant', 'quán ăn', 'eatery']):
        return 'Restaurant'
    elif any(word in name_lower for word in ['quán']):
        # "Quán" is ambiguous - could be coffee shop or restaurant
        # If it has coffee-related terms, it's likely a coffee shop
        if any(word in name_lower for word in ['phê', 'cafe', 'coffee', 'cà phê']):
            return 'Cafe'
        else:
            return 'Restaurant'
    elif any(word in name_lower for word in ['bún', 'phở', 'cơm', 'bánh']):
        return 'Restaurant'
    elif any(word in name_lower for word in ['store', 'shop', 'cửa hàng']):
        return 'Convenience store'
    else:
        return 'Restaurant'  # Default


if __name__ == "__main__":
    # Test the parser
    test_url = "https://www.google.com/maps/place/Qu%C3%A1n+B%E1%BB%A5i+Garden/@10.8046882,106.7360579,18.45z/data=!4m6!3m5!1s0x317526176671636b:0x471be660ffc59db!8m2!3d10.805121!4d106.735759!16s%2Fg%2F11c0rh7rdx?entry=ttu&g_ep=EgoyMDI1MTAyOS4yIKXMDSoASAFQAw%3D%3D"
    
    print("Testing URL Parser...\n")
    print("="*60)
    
    print("\n1. Parsing URL...")
    basic_info = parse_google_maps_url(test_url)
    print(f"   Place: {basic_info['place_name']}")
    print(f"   Location: ({basic_info['latitude']}, {basic_info['longitude']})")
    print(f"   Place ID: {basic_info['place_id']}")
    
    print("\n2. Scraping details from Google Maps...")
    full_info = scrape_place_details_from_google(test_url)
    print(f"   Rating: {full_info.get('avg_rating', 'N/A')}")
    print(f"   Reviews: {full_info.get('reviews_number', 0)}")
    print(f"   Last Avg Rating: {full_info.get('last_avg_rating', 'N/A')}")
    print(f"   Last 1 Reviews: {full_info.get('last_1_reviews_number', 0)}")
    print(f"   Last 2 Reviews: {full_info.get('last_2_reviews_number', 0)}")
    print(f"   Category: {full_info.get('category', 'N/A')}")
    print(f"   Address: {full_info.get('address', 'N/A')}")
    
    print("\n3. Extracting location info from address...")
    if full_info.get('address'):
        ward = extract_ward_from_address(full_info['address'])
        province = extract_province_from_address(full_info['address'])
        print(f"   Ward: {ward}")
        print(f"   Province: {province}")
    
    print("\n4. Inferring category...")
    category = infer_category_from_name(full_info['place_name'], full_info.get('category'))
    print(f"   Inferred Category: {category}")
    
    print("\n5. All Features for Model:")
    print(f"   ✓ avg_rating: {full_info.get('avg_rating', 'N/A')}")
    print(f"   ✓ reviews_number: {full_info.get('reviews_number', 0)}")
    print(f"   ✓ last_avg_rating: {full_info.get('last_avg_rating', 'N/A')}")
    print(f"   ✓ last_1_reviews_number: {full_info.get('last_1_reviews_number', 0)}")
    print(f"   ✓ last_2_reviews_number: {full_info.get('last_2_reviews_number', 0)}")
    print(f"   ✓ latitude: {full_info.get('latitude')}")
    print(f"   ✓ longitude: {full_info.get('longitude')}")
    print(f"   ✓ location_type_resolved: {category}")
    print(f"   ✓ province_name: {extract_province_from_address(full_info.get('address', ''))}")
    print(f"   ✓ ward_name: {extract_ward_from_address(full_info.get('address', ''))}")
    
    # Calculate H3 index - resolution 9
    try:
        import h3
        lat = full_info.get('latitude', 0)
        lon = full_info.get('longitude', 0)
        if lat and lon and lat != 0 and lon != 0:
            h3_idx = h3.latlng_to_cell(lat, lon, 9)
            print(f"   ✓ idx_r9_hex: {h3_idx}")
        else:
            print(f"   ✓ idx_r9_hex: N/A (coordinates missing)")
    except Exception as e:
        print(f"   ✓ idx_r9_hex: N/A (error: {e})")
    
    print("\n" + "="*60)
    print("✓ All tests complete!")

