from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import cv2
import numpy as np
import pytesseract
from PIL import Image
import io
import re

app = FastAPI(title="Smart OCR System", version="4.0")

class OCRRequest(BaseModel):
    image_url: str = None

def preprocess_image(image):
    """Tiền xử lý ảnh để cải thiện chất lượng OCR"""
    # Chuyển sang grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Giảm nhiễu
    denoised = cv2.medianBlur(gray, 3)
    
    # Tăng độ tương phản
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(denoised)
    
    # Threshold adaptive
    thresh = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY, 11, 2)
    
    return thresh

def postprocess_text(text):
    """Hậu xử lý văn bản để sửa lỗi OCR"""
    # Sửa lỗi common OCR
    corrections = {
        'ỔNG TY': 'CÔNG TY',
        'TNHI': 'TNHH',
        'ĐẢU': 'ĐẦU',
        'THƯONG': 'THƯƠNG',
        'VIẸT': 'VIỆT',
        'VAM': 'NAM',
        'ĐẠl': 'ĐẠI',
        'THĂNG': 'THĂNG',
        'THAMH': 'THANH',
        'mười chín': 'mười chín',
        'sáu mươi': 'sáu mươi'
    }
    
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    
    # Chuẩn hóa khoảng trắng
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

@app.get("/")
def root():
    return {"message": "Smart OCR System - Phiên bản cải tiến", "status": "working"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": "4.0"}

@app.post("/api/ocr")
async def ocr_endpoint(request: OCRRequest = None, file: UploadFile = None):
    try:
        if file:
            # Xử lý file upload
            image_data = await file.read()
            image = Image.open(io.BytesIO(image_data))
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        elif request and request.image_url:
            # Xử lý URL (tạm thời dùng ảnh mẫu)
            return {
                "success": True,
                "text": "Chức năng URL đang được phát triển",
                "status": "info"
            }
        else:
            raise HTTPException(status_code=400, detail="Thiếu file ảnh hoặc image_url")
        
        # Tiền xử lý ảnh
        processed_image = preprocess_image(image_cv)
        
        # OCR với multiple configs để tối ưu độ chính xác
        configs = [
            '--oem 3 --psm 6',  # Khối văn bản thống nhất
            '--oem 3 --psm 4',  # Một cột văn bản
            '--oem 3 --psm 8'   # Một từ
        ]
        
        best_text = ""
        best_confidence = 0
        
        for config in configs:
            ocr_data = pytesseract.image_to_data(processed_image, output_type=pytesseract.Output.DICT, config=config, lang='vie')
            
            # Tính độ tin cậy trung bình
            confidences = [int(conf) for conf in ocr_data['conf'] if int(conf) > 0]
            if confidences:
                avg_confidence = sum(confidences) / len(confidences)
                
                # Lấy text từ các phần có độ tin cậy cao
                text_parts = []
                for i, conf in enumerate(ocr_data['conf']):
                    if int(conf) > 50:  # Chỉ lấy text có độ tin cậy > 50%
                        text_parts.append(ocr_data['text'][i])
                
                current_text = ' '.join([text for text in text_parts if text.strip()])
                
                if avg_confidence > best_confidence and current_text:
                    best_confidence = avg_confidence
                    best_text = current_text
        
        # Hậu xử lý văn bản
        cleaned_text = postprocess_text(best_text)
        
        return {
            "success": True,
            "text": cleaned_text,
            "confidence": round(best_confidence, 2),
            "version": "4.0",
            "language": "vie",
            "characters_count": len(cleaned_text.replace(" ", ""))
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Lỗi xử lý OCR"
        }

@app.post("/api/upload-ocr")
async def upload_ocr(file: UploadFile = File(...)):
    """Endpoint chuyên cho upload file ảnh"""
    return await ocr_endpoint(file=file)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
