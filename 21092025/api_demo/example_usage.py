"""
Example usage of the Beer Sales Prediction API
Shows how to integrate the API into your application
"""
import requests
import json


class BeerSalesPredictionClient:
    """Client for interacting with Beer Sales Prediction API"""
    
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
        
    def check_health(self):
        """Check if API is running"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def predict_single(self, google_maps_url, google_api_key=None):
        """
        Predict beer sales potential for a single POI
        
        Args:
            google_maps_url: Google Maps place URL
            google_api_key: Optional Google API key for enhanced data
            
        Returns:
            Dictionary with prediction results
        """
        payload = {
            "google_maps_url": google_maps_url,
            "google_api_key": google_api_key
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/predict", 
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def predict_batch(self, google_maps_urls, google_api_key=None):
        """
        Predict beer sales potential for multiple POIs
        
        Args:
            google_maps_urls: List of Google Maps place URLs
            google_api_key: Optional Google API key
            
        Returns:
            Dictionary with batch prediction results
        """
        try:
            response = requests.post(
                f"{self.api_url}/predict-batch",
                params={"google_api_key": google_api_key},
                json=google_maps_urls,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


def example_1_single_prediction():
    """Example 1: Simple single prediction"""
    print("\n" + "="*60)
    print("Example 1: Single Prediction")
    print("="*60)
    
    client = BeerSalesPredictionClient()
    
    # Check if API is running
    if not client.check_health():
        print("❌ API is not running. Start it with: python main.py")
        return
    
    # Predict for a restaurant
    url = "https://www.google.com/maps/place/Qu%C3%A1n+B%E1%BB%A5i+Garden/@10.8046882,106.7360579,18.45z/data=!4m6!3m5!1s0x317526176671636b:0x471be660ffc59db!8m2!3d10.805121!4d106.735759"
    
    print(f"\n🔍 Analyzing place...")
    result = client.predict_single(url)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    # Display results
    print(f"\n✅ Prediction Complete!")
    print(f"   Place: {result['place_info']['name']}")
    print(f"   Location: {result['place_info']['category']}")
    print(f"   Rating: {result['place_info']['rating']} ⭐")
    print(f"\n   🎯 Result: {result['prediction_label']}")
    print(f"   📊 Confidence: {result['confidence_percentage']}")
    print(f"   🎚️  {result['risk_level']}")
    print(f"\n   💡 {result['recommendation']}")


def example_2_batch_prediction():
    """Example 2: Batch prediction for multiple locations"""
    print("\n" + "="*60)
    print("Example 2: Batch Prediction")
    print("="*60)
    
    client = BeerSalesPredictionClient()
    
    if not client.check_health():
        print("❌ API is not running.")
        return
    
    # List of URLs to analyze
    urls = [
        "https://www.google.com/maps/place/Qu%C3%A1n+B%E1%BB%A5i+Garden/@10.8046882,106.7360579,18.45z/data=!4m6!3m5!1s0x317526176671636b:0x471be660ffc59db!8m2!3d10.805121!4d106.735759",
        "https://www.google.com/maps/place/Highlands+Coffee/@10.7764242,106.7002266,17z/data=!3m1!4b1!4m6!3m5!1s0x31752f4175e58f67:0xfd3cf7e83f9923d3!8m2!3d10.7764242!4d106.7002266",
        "https://www.google.com/maps/place/Bep+Me+In/@10.7764833,106.7008719,17z/data=!3m1!4b1!4m6!3m5!1s0x31752f62a90a5d5f:0x37a5c618535287f8!8m2!3d10.7764833!4d106.7008719"
    ]
    
    print(f"\n🔍 Analyzing {len(urls)} locations...")
    results = client.predict_batch(urls)
    
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        return
    
    print(f"\n✅ Batch Analysis Complete!")
    print(f"   Total: {results['total']} | Successful: {results['successful']}")
    
    # Display summary
    print("\n📊 SUMMARY:")
    print("-" * 60)
    
    for i, result in enumerate(results['results'], 1):
        if result.get('success'):
            print(f"\n{i}. {result['place_info']['name']}")
            print(f"   {result['prediction_label']} - {result['confidence_percentage']}")
            print(f"   {result['risk_level']}")


def example_3_decision_making():
    """Example 3: Using predictions for business decisions"""
    print("\n" + "="*60)
    print("Example 3: Business Decision Making")
    print("="*60)
    
    client = BeerSalesPredictionClient()
    
    if not client.check_health():
        print("❌ API is not running.")
        return
    
    # Candidate locations for beer distribution
    candidates = {
        "Restaurant A": "https://www.google.com/maps/place/Qu%C3%A1n+B%E1%BB%A5i+Garden/@10.8046882,106.7360579,18.45z/data=!4m6!3m5!1s0x317526176671636b:0x471be660ffc59db!8m2!3d10.805121!4d106.735759",
        "Cafe B": "https://www.google.com/maps/place/Highlands+Coffee/@10.7764242,106.7002266,17z/data=!3m1!4b1!4m6!3m5!1s0x31752f4175e58f67:0xfd3cf7e83f9923d3!8m2!3d10.7764242!4d106.7002266"
    }
    
    print("\n🎯 Evaluating candidate locations for beer distribution...\n")
    
    high_potential = []
    medium_potential = []
    low_potential = []
    
    for name, url in candidates.items():
        result = client.predict_single(url)
        
        if "error" not in result:
            confidence = result['confidence']
            
            print(f"📍 {name}")
            print(f"   Confidence: {result['confidence_percentage']}")
            print(f"   Risk Level: {result['risk_level']}")
            print()
            
            # Categorize
            if confidence >= 0.7:
                high_potential.append(name)
            elif confidence >= 0.4:
                medium_potential.append(name)
            else:
                low_potential.append(name)
    
    # Business recommendations
    print("\n" + "="*60)
    print("📋 BUSINESS RECOMMENDATIONS")
    print("="*60)
    
    if high_potential:
        print(f"\n✅ HIGH PRIORITY (Confidence ≥70%):")
        for loc in high_potential:
            print(f"   • {loc} - Immediate distribution recommended")
    
    if medium_potential:
        print(f"\n⚠️  MEDIUM PRIORITY (Confidence 40-70%):")
        for loc in medium_potential:
            print(f"   • {loc} - Consider after market research")
    
    if low_potential:
        print(f"\n❌ LOW PRIORITY (Confidence <40%):")
        for loc in low_potential:
            print(f"   • {loc} - Not recommended at this time")


def example_4_export_results():
    """Example 4: Export predictions to CSV"""
    print("\n" + "="*60)
    print("Example 4: Export Results to CSV")
    print("="*60)
    
    import csv
    from datetime import datetime
    
    client = BeerSalesPredictionClient()
    
    if not client.check_health():
        print("❌ API is not running.")
        return
    
    urls = [
        "https://www.google.com/maps/place/Qu%C3%A1n+B%E1%BB%A5i+Garden/@10.8046882,106.7360579,18.45z/data=!4m6!3m5!1s0x317526176671636b:0x471be660ffc59db!8m2!3d10.805121!4d106.735759"
    ]
    
    results = client.predict_batch(urls)
    
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        return
    
    # Export to CSV
    filename = f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Place Name', 'Latitude', 'Longitude', 'Category', 
            'Rating', 'Reviews', 'Prediction', 'Confidence', 'Risk Level'
        ])
        
        for result in results['results']:
            if result.get('success'):
                writer.writerow([
                    result['place_info']['name'],
                    result['place_info']['latitude'],
                    result['place_info']['longitude'],
                    result['place_info']['category'],
                    result['place_info']['rating'],
                    result['place_info']['reviews'],
                    result['prediction_label'],
                    result['confidence_percentage'],
                    result['risk_level']
                ])
    
    print(f"\n✅ Results exported to: {filename}")


def main():
    """Run all examples"""
    print("\n🍺" * 30)
    print("  BEER SALES PREDICTION API - USAGE EXAMPLES")
    print("🍺" * 30)
    
    try:
        # Example 1: Single prediction
        example_1_single_prediction()
        
        # Example 2: Batch prediction
        example_2_batch_prediction()
        
        # Example 3: Business decision making
        example_3_decision_making()
        
        # Example 4: Export to CSV
        example_4_export_results()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)
        print("\n💡 Next steps:")
        print("   - Integrate this client into your application")
        print("   - Add Google API key for better accuracy")
        print("   - Customize decision thresholds for your use case")
        print()
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")


if __name__ == "__main__":
    main()



