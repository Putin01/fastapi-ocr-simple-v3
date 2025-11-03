from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="OCR API", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoints
@app.get("/")
async def root():
    return {"message": "OCR API - Deploy thanh cong!", "status": "working"}

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
            {"path": "/api/ocr", "method": "POST", "description": "OCR tu URL anh"},
            {"path": "/api/extract-text", "method": "POST", "description": "Test OCR endpoint"}
        ]
    }

@app.post("/api/extract-text")
async def extract_text_simple():
    return {
        "success": True, 
        "text": "Day la van ban mau tu OCR",
        "message": "OCR endpoint da san sang!",
        "language": "vi"
    }

@app.post("/api/ocr")
async def ocr_from_url(image_url: str = None):
    if not image_url:
        return {
            "success": False,
            "error": "Thieu image_url parameter",
            "usage": "Gui POST voi {'image_url': 'https://...'}"
        }
    
    return {
        "success": True,
        "text": f"OCR tu anh: {image_url} (chuc nang dang phat trien)",
        "image_url": image_url,
        "status": "processing"
    }

# Handler cho Vercel
import os
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
