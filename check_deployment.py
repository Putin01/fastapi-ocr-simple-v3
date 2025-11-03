import requests
import sys

def check_deployment():
    urls = [
        "https://fastapi-ocr-simple-v3.vercel.app",
        "https://fastapi-ocr-simple-v3-o7kaIQgu2-putln01s-projects.vercel.app"
    ]
    
    for url in urls:
        try:
            print(f"🔍 Testing {url}...")
            response = requests.get(url, timeout=10)
            print(f"✅ Status: {response.status_code}")
            if response.status_code == 200:
                print(f"📄 Response: {response.text}")
                return True
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    success = check_deployment()
    sys.exit(0 if success else 1)
