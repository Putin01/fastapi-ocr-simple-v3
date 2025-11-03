from fastapi import FastAPI
import os

app = FastAPI(title="OCR API Simple", version="3.1.0")

@app.get("/")
def root():
    return {
        "message": "🚀 OCR API Version 3 - DEPLOY THÀNH CÔNG!", 
        "status": "success",
        "version": "3.1.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "version": "3.1.0"}

@app.get("/tinh-nang")
def features():
    return {
        "features": ["ocr", "ai", "simple-api"], 
        "version": "3.1.0"
    }

# Important for Vercel
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
