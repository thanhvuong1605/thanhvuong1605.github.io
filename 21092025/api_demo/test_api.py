"""
Test script for Beer Sales Prediction API
"""
import requests
import json
from time import sleep


# API Configuration
API_URL = "http://localhost:8000"


def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_health_check():
    """Test health check endpoint"""
    print_section("1. Testing Health Check")
    
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✓ API is healthy!")
            print(f"  Status: {data['status']}")
            print(f"  Model Loaded: {data['model_loaded']}")
            if data.get('model_info'):
                print(f"  Model AUC: {data['model_info']['test_auc']:.4f}")
                print(f"  Model Accuracy: {data['model_info']['test_accuracy']:.4f}")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to API. Is it running?")
        print("  Start with: python main.py")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_prediction(url, description):
    """Test prediction endpoint"""
    print(f"\n🔍 Testing: {description}")
    print(f"📍 URL: {url[:80]}...")
    
    try:
        payload = {
            "google_maps_url": url,
            "google_api_key": None
        }
        
        response = requests.post(f"{API_URL}/predict", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n📊 RESULTS:")
            print(f"  Place: {data['place_info']['name']}")
            print(f"  Location: ({data['place_info']['latitude']}, {data['place_info']['longitude']})")
            print(f"  Category: {data['place_info']['category']}")
            print(f"  Rating: {data['place_info']['rating']} ⭐")
            print(f"  Reviews: {data['place_info']['reviews']}")
            print(f"\n  🎯 PREDICTION: {data['prediction_label']}")
            print(f"  📈 Confidence: {data['confidence_percentage']}")
            print(f"  🎚️  Risk Level: {data['risk_level']}")
            print(f"  💡 Recommendation: {data['recommendation']}")
            
            return True
        else:
            print(f"✗ Prediction failed: {response.status_code}")
            print(f"  Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_batch_prediction():
    """Test batch prediction endpoint"""
    print_section("4. Testing Batch Prediction")
    
    urls = [
        "https://www.google.com/maps/place/Qu%C3%A1n+B%E1%BB%A5i+Garden/@10.8046882,106.7360579,18.45z/data=!4m6!3m5!1s0x317526176671636b:0x471be660ffc59db!8m2!3d10.805121!4d106.735759",
        "https://www.google.com/maps/place/Bep+Me+In/@10.7764833,106.7008719,17z/data=!3m1!4b1!4m6!3m5!1s0x31752f62a90a5d5f:0x37a5c618535287f8!8m2!3d10.7764833!4d106.7008719!16s%2Fg%2F1td3kq45"
    ]
    
    try:
        response = requests.post(
            f"{API_URL}/predict-batch",
            params={"google_api_key": None},
            json=urls
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Batch prediction successful!")
            print(f"  Total: {data['total']}")
            print(f"  Successful: {data['successful']}")
            
            for i, result in enumerate(data['results'], 1):
                if result.get('success'):
                    print(f"\n  [{i}] {result['place_info']['name']}: {result['prediction_label']} ({result['confidence_percentage']})")
            
            return True
        else:
            print(f"✗ Batch prediction failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "🍺"*30)
    print("  BEER SALES PREDICTION API - TEST SUITE")
    print("🍺"*30)
    
    # Test 1: Health Check
    if not test_health_check():
        print("\n❌ API is not running. Please start it first:")
        print("   python main.py")
        return
    
    sleep(0.5)
    
    # Test 2: Restaurant (likely beer seller)
    print_section("2. Testing Restaurant Prediction")
    test_prediction(
        "https://www.google.com/maps/place/Qu%C3%A1n+B%E1%BB%A5i+Garden/@10.8046882,106.7360579,18.45z/data=!4m6!3m5!1s0x317526176671636b:0x471be660ffc59db!8m2!3d10.805121!4d106.735759!16s%2Fg%2F11c0rh7rdx",
        "Quán Bụi Garden (Restaurant)"
    )
    
    sleep(0.5)
    
    # Test 3: Cafe (less likely)
    print_section("3. Testing Cafe Prediction")
    test_prediction(
        "https://www.google.com/maps/place/Highlands+Coffee/@10.7764242,106.7002266,17z/data=!3m1!4b1!4m6!3m5!1s0x31752f4175e58f67:0xfd3cf7e83f9923d3!8m2!3d10.7764242!4d106.7002266",
        "Highlands Coffee (Cafe)"
    )
    
    sleep(0.5)
    
    # Test 4: Batch prediction
    test_batch_prediction()
    
    # Summary
    print_section("✅ TEST SUITE COMPLETED")
    print("\n💡 Tips:")
    print("  - Check http://localhost:8000/docs for interactive API documentation")
    print("  - Add Google API key for more accurate real-time data")
    print("  - Use batch endpoint for processing multiple locations")
    print()


if __name__ == "__main__":
    main()

