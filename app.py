from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "OCR API - Working", "status": "success"}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/test")
async def test():
    return {"test": "success", "api": "working"}

# ========== OCR ENDPOINTS ==========
@app.get("/api/ocr-info")
async def ocr_info():
    return {
        "name": "OCR API",
        "version": "1.0", 
        "endpoints": [
            "/api/ocr",
            "/api/extract-text"
        ]
    }

@app.post("/api/extract-text")
async def extract_text():
    return {
        "success": True,
        "text": "This is sample OCR text",
        "message": "OCR endpoint is working"
    }

@app.post("/api/ocr")
async def ocr_endpoint(image_url: str = None):
    if image_url:
        return {
            "success": True,
            "text": f"OCR processing for: {image_url}",
            "image_url": image_url,
            "status": "processed"
        }
    else:
        return {
            "success": False,
            "error": "Please provide image_url"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
