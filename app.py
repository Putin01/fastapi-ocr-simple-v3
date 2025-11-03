from fastapi import FastAPI

app = FastAPI()

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
def ocr_endpoint():
    return {
        "success": True, 
        "text": "OCR processing completed",
        "status": "success"
    }
