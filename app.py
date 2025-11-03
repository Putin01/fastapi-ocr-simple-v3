from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "OCR API - Fixed", "status": "working"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/test")
def test():
    return {"test": "success", "api": "working"}

@app.get("/api/ocr-info")
def ocr_info():
    return {"name": "OCR API", "endpoints": ["/api/ocr"]}

@app.post("/api/extract-text")
def extract_text():
    return {"text": "Sample OCR text", "success": True}

@app.post("/api/ocr")
def ocr_endpoint(image_url: str = None):
    return {"text": f"OCR from {image_url}", "success": True}
