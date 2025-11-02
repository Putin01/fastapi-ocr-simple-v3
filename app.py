from fastapi import FastAPI
import uvicorn
import os

app = FastAPI(title="OCR API V3")

@app.get("/")
async def home():
    return {"message": "OCR API Version 3 - Fresh Start!", "status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "3.0.0"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
