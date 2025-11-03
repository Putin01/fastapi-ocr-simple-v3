from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Smart OCR API 3.1 - Fixed Deployment", "status": "success"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "3.1.0"}

@app.get("/tinh-nang")
def features():
    return {
        "features": ["ocr", "ai_classification", "vietnamese_support"],
        "version": "3.1.0",
        "status": "active"
    }
