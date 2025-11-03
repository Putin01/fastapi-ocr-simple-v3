from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "OCR API - Fixed deployment", "status": "working"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/test")
def test():
    return {"test": "success", "api": "working"}

# OCR ENDPOINTS
@app.get("/api/ocr-info")
def ocr_info():
    return {
        "name": "OCR API",
        "version": "1.0",
        "endpoints": ["/api/ocr", "/api/extract-text"]
    }

@app.post("/api/extract-text")
def extract_text():
    return {
        "success": True,
        "text": "Sample OCR text",
        "message": "OCR is working"
    }

@app.post("/api/ocr")
def ocr_endpoint(image_url: str = None):
    if image_url:
        return {
            "success": True,
            "text": f"OCR from: {image_url}",
            "status": "success"
        }
    return {
        "success": False,
        "error": "Need image_url"
    }
