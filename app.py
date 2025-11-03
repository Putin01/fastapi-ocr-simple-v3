from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "OCR API 3.1 - ULTRA SIMPLE", "status": "success"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": "3.1.0"}

@app.get("/tinh-nang")
def features():
    return {"features": ["ocr", "ai"], "version": "3.1.0"}
