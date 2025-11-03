from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import aiofiles
import os
import logging
from document_classifier import classifier

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Smart OCR với AI Classification", 
    version="3.1.0",
    description="API OCR thông minh với phân loại tài liệu AI - Phiên bản tiếng Việt"
)

@app.get("/")
async def root():
    return {
        "thông_báo": "Smart OCR API Phiên bản 3.1 - Với AI Phân loại Tài liệu!", 
        "trạng_thái": "thành_công",
        "phiên_bản": "3.1.0",
        "tính_năng": ["ocr", "ai_phân_loại", "xử_lý_tiếng_việt"]
    }

@app.get("/health")
async def health_check():
    return {
        "trạng_thái": "khỏe_mạnh", 
        "phiên_bản": "3.1.0",
        "dịch_vụ": ["ocr", "ai_phân_loại", "api_rest"],
        "ngôn_ngữ": "vi"
    }

@app.post("/phan-loai")
async def phan_loai_tai_lieu(file: UploadFile = File(...)):
    """Phân loại tài liệu AI - Phiên bản tiếng Việt"""
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Không có file được cung cấp")
        
        # Phân loại AI
        ket_qua_phan_loai = await classifier.classify_document(file)
        
        return {
            "tên_file": file.filename,
            "phân_loại": ket_qua_phan_loai,
            "trạng_thái": "thành_công",
            "phương_thức": "ai_phân_loại"
        }
        
    except Exception as e:
        logger.error(f"Lỗi phân loại: {e}")
        raise HTTPException(status_code=500, detail=f"Phân loại thất bại: {str(e)}")

@app.post("/ocr-thong-minh")
async def ocr_thong_minh(file: UploadFile = File(...)):
    """OCR thông minh kết hợp AI classification - Tiếng Việt"""
    try:
        # Lưu file tạm để xử lý
        file_path = f"temp_{file.filename}"
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # TODO: Thêm OCR processing thực tế
        # Trong tương lai sẽ tích hợp OCR thật
        ocr_result = {
            "văn_bản_trích_xuất": f"Mẫu văn bản từ {file.filename}",
            "số_từ": 15,
            "thời_gian_xử_lý": 0.5,
            "ngôn_ngữ": "vi"
        }
        
        # AI Phân loại
        ket_qua_phan_loai = await classifier.classify_document(file, ocr_result["văn_bản_trích_xuất"])
        
        # Kết hợp kết quả
        ket_qua = {
            "tên_file": file.filename,
            "kết_quả_ocr": ocr_result,
            "phân_loại_ai": ket_qua_phan_loai,
            "loại_xử_lý": "ocr_thông_minh_v1",
            "trạng_thái": "hoàn_thành"
        }
        
        # Dọn dẹp
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return ket_qua
        
    except Exception as e:
        logger.error(f"Lỗi OCR thông minh: {e}")
        raise HTTPException(status_code=500, detail=f"Xử lý thông minh thất bại: {str(e)}")

@app.get("/tinh-nang")
async def danh_sach_tinh_nang():
    """Danh sách tính năng có sẵn"""
    return {
        "tính_năng": {
            "ocr_cơ_bản": "Đang phát triển",
            "phân_loại_ai": "Hoạt động (Rule-based)",
            "ocr_thông_minh": "Đang phát triển", 
            "xử_lý_tiếng_việt": "Hoạt động",
            "api_rest": "Hoạt động"
        },
        "phiên_bản": "3.1.0",
        "trạng_thái": "đang_phát_triển"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
