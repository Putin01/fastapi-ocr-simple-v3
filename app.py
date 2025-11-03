from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="OCR API v3", version="3.0")

class OCRRequest(BaseModel):
    image_url: str

@app.get("/")
def root():
    return {"message": "OCR API v3 - NEW DEPLOYMENT", "status": "working"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": "3.0"}

@app.post("/api/ocr")
def ocr_endpoint(request: OCRRequest):
    return {
        "success": True,
        "text": f"OCR processing for: {request.image_url}",
        "status": "success",
        "version": "3.0"
    }
