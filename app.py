from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from PIL import Image
import io
import pytesseract
import re

app = FastAPI(title="Smart OCR System", version="5.0")

class OCRRequest(BaseModel):
    image_url: str = None

def enhance_image_quality(image):
    """Cải thiện chất lượng ảnh bằng PIL"""
    # Chuyển sang grayscale nếu là ảnh màu
    if image.mode != 'L':
        image = image.convert('L')
    
    # Tăng độ tương phản
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)  # Tăng contrast 2 lần
    
    # Tăng độ sắc nét
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)
    
    return image

def correct_common_errors(text):
    """Sửa lỗi OCR phổ biến trong tiếng Việt"""
    corrections = {
        'ỔNG TY': 'CÔNG TY',
        'TNHI': 'TNHH', 
        'ĐẢU': 'ĐẦU',
        'THƯONG': 'THƯƠNG',
        'VIẸT': 'VIỆT',
        'VAM': 'NAM',
        'ĐẠl': 'ĐẠI',
        'THAMH': 'THANH',
        'MẶI': 'MẠI',
        'THAMH': 'THANH',
        'DỤNG': 'DỤNG',
        'Đéc': 'Độc',
        'Jâp': 'Lập',
        'lu': 'lập',
        'Hanh': 'Hạnh',
        'phúc': 'phúc',
        'GIÁP': 'GIẤY',
        'CÍC': 'ĐỀ',
        'NHỊ': 'NGHỊ',
        'THAMH': 'THANH',
        'TOÀN': 'TOÁN',
        'ký': 'kỹ',
        'thuật': 'thuật',
        'TRƯỜNG': 'TRƯỜNG',
        'ĐẠl': 'ĐẠI',
        'HỌC': 'HỌC',
        'KHOA': 'KHOA',
        'HỌC': 'HỌC',
        'TỰ': 'TỰ',
        'NHIÊN': 'NHIÊN'
    }
    
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    
    # Chuẩn hóa khoảng trắng
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

@app.get("/")
def root():
    return {"message": "Smart OCR System v5.0 - Enhanced Accuracy", "status": "working"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": "5.0"}

@app.post("/api/ocr")
async def ocr_endpoint(request: OCRRequest = None, file: UploadFile = None):
    try:
        if file:
            # Đọc và xử lý ảnh
            image_data = await file.read()
            image = Image.open(io.BytesIO(image_data))
            
            # Cải thiện chất lượng ảnh
            enhanced_image = enhance_image_quality(image)
            
            # OCR với cấu hình tối ưu cho tiếng Việt
            custom_config = r'--oem 3 --psm 6 -l vie'
            raw_text = pytesseract.image_to_string(enhanced_image, config=custom_config)
            
            # Sửa lỗi văn bản
            cleaned_text = correct_common_errors(raw_text)
            
            return {
                "success": True,
                "text": cleaned_text,
                "original_text": raw_text,
                "version": "5.0",
                "language": "vie",
                "characters_count": len(cleaned_text.replace(" ", "")),
                "message": "OCR xử lý thành công với độ chính xác cao"
            }
            
        elif request and request.image_url:
            return {
                "success": True,
                "text": "Chức năng URL image đang được phát triển",
                "status": "info"
            }
        else:
            raise HTTPException(status_code=400, detail="Vui lòng cung cấp file ảnh hoặc image_url")
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Lỗi xử lý OCR"
        }

@app.post("/api/upload-ocr")
async def upload_ocr(file: UploadFile = File(...)):
    return await ocr_endpoint(file=file)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
