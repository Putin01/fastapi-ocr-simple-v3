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
    return {"message": "OCR API - Deploy thành công!", "status": "working"}

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
            {"path": "/api/ocr", "method": "POST", "description": "OCR t? URL ?nh"},
            {"path": "/api/extract-text", "method": "POST", "description": "Test OCR endpoint"}
        ]
    }

@app.post("/api/extract-text")
async def extract_text_simple():
    return {
        "success": True, 
        "text": "Ðây là van b?n m?u t? OCR",
        "message": "OCR endpoint dã s?n sàng!",
        "language": "vi"
    }

@app.post("/api/ocr")
async def ocr_from_url(image_url: str = None):
    if not image_url:
        return {
            "success": False,
            "error": "Thi?u image_url parameter",
            "usage": "G?i POST v?i {'image_url': 'https://...'}"
        }
    
    return {
        "success": True,
        "text": f"OCR t? ?nh: {image_url} (ch?c nang dang phát tri?n)",
        "image_url": image_url,
        "status": "processing"
    }

# Handler cho Vercel
import os
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
