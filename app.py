from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class OCRRequest(BaseModel):
    image_url: str

@app.get("/")
def root():
    return {"message": "OCR API - Simple", "status": "working"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": "2.0"}

@app.get("/api/ocr-info")
def ocr_info():
    return {
        "name": "OCR API",
        "version": "2.0",
        "endpoints": [
            {"path": "/api/ocr", "method": "POST"},
            {"path": "/api/extract-text", "method": "POST"}
        ]
    }

@app.post("/api/extract-text")
def extract_text():
    return {
        "success": True,
        "text": "This is sample OCR text",
        "message": "OCR is working!"
    }

@app.post("/api/ocr")
def ocr_endpoint(request: OCRRequest):
    return {
        "success": True,
        "text": f"OCR processing for {request.image_url}",
        "status": "success",
        "image_url": request.image_url
    }
