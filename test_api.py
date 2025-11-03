import requests

def test_api():
    base_url = "https://fastapi-ocr-simple-v3.up.railway.app"
    
    print("🧪 Testing Smart OCR API...")
    
    try:
        # Test root endpoint
        response = requests.get(f"{base_url}/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test health endpoint
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        print("🎉 API is working perfectly!")
        
    except Exception as e:
        print(f"❌ API test failed: {e}")

if __name__ == "__main__":
    test_api()
