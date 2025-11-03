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

# Root endpoint
@app.get("/")
async def root():
    return {"message": "OCR API - Deploy thành công!", "status": "working"}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/test")
async def test():
    return {"test": "success", "api": "working"}

# OCR Endpoints
@app.get("/api/ocr-info")
async def ocr_info():
    return {
        "name": "OCR API", 
        "version": "1.0",
        "endpoints": ["/api/ocr", "/api/extract-text"]
    }

@app.post("/api/extract-text")
async def extract_text_simple():
    return {
        "success": True, 
        "text": "Ðây là van b?n m?u t? OCR",
        "message": "OCR endpoint dã s?n sàng!"
    }

# Handler cho Vercel
import os
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
