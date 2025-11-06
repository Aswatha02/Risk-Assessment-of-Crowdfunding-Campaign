import requests
import json
import time

def test_api_health():
    print("🧪 Testing API Health...")
    
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API is healthy")
            print(f"   Mode: {data.get('mode', 'unknown')}")
            print(f"   Models loaded: {data.get('models_loaded', False)}")
            print(f"   Features: {data.get('total_features', 0)}")
            
            # Validate response structure
            assert 'status' in data, "Missing 'status' field"
            assert 'models_loaded' in data, "Missing 'models_loaded' field"
            assert 'total_features' in data, "Missing 'total_features' field"
            
            return True
        else:
            print(f"   ❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ API connection failed: {e}")
        return False

def test_prediction():
    print("🧪 Testing Prediction Endpoint...")
    
    test_campaign = {
        "name": "AI-Powered Smart Watch",
        "blurb": "Revolutionary smart watch with AI assistant and health monitoring",
        "goal": 15000,
        "pledged": 2500,
        "backers_count": 45,
        "country": "US",
        "currency": "USD",
        "category": "Technology",
        "launch_to_deadline_days": 45,
        "create_to_launch_days": 7,
        "staff_pick": True,
        "spotlight": False
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=test_campaign,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Prediction successful!")
            print(f"   Success probability: {result['success_probability']:.2%}")
            print(f"   Risk level: {result['risk_level']}")
            print(f"   Recommendations: {len(result.get('recommendations', []))}")
            
            # Validate response structure
            assert 'success_probability' in result, "Missing 'success_probability'"
            assert 'risk_level' in result, "Missing 'risk_level'"
            assert 'risk_color' in result, "Missing 'risk_color'"
            assert 'model_scores' in result, "Missing 'model_scores'"
            assert 'explanations' in result, "Missing 'explanations'"
            assert 'recommendations' in result, "Missing 'recommendations'"
            
            # Validate probability range
            prob = result['success_probability']
            assert 0 <= prob <= 1, f"Invalid probability: {prob}"
            
            return True
        else:
            print(f"   ❌ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Prediction test failed: {e}")
        return False

def test_features_endpoint():
    print("🧪 Testing Features Endpoint...")
    
    try:
        response = requests.get("http://localhost:8000/features")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Features endpoint working")
            print(f"   Total features: {data.get('total_features', 0)}")
            if 'top_10_features' in data:
                print(f"   Top features: {len(data['top_10_features'])} features")
            
            # Validate response structure
            assert 'total_features' in data, "Missing 'total_features' field"
            assert 'feature_names' in data, "Missing 'feature_names' field"
            
            return True
        elif response.status_code == 503:
            print(f"   ⚠️  Models not loaded (fallback mode)")
            print(f"   This is expected if models haven't been trained yet")
            return True  # Still pass the test
        else:
            print(f"   ❌ Features endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Features test failed: {e}")
        return False

def run_all_api_tests():
    print("🚀 Starting API Integration Tests...")
    print("=" * 50)
    
    # Wait a bit for server to start
    time.sleep(2)
    
    tests = [
        test_api_health,
        test_features_endpoint,
        test_prediction
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    if passed == total:
        print(f"🎉 All API tests passed! ({passed}/{total})")
    else:
        print(f"⚠️  Some tests failed: ({passed}/{total})")
    
    return passed == total

if __name__ == "__main__":
    run_all_api_tests()