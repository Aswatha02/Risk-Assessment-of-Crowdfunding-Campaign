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
            print(f"   Models loaded: {data['models_loaded']}")
            print(f"   Features: {data['total_features']}")
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
            print(f"   Recommendations: {len(result['recommendations'])}")
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
            print(f"   Total features: {data['total_features']}")
            print(f"   Top features: {data['top_10_features']}")
            return True
        else:
            print(f"   ❌ Features endpoint failed: {response.status_code}")
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