# document_classifier.py - Bộ phân loại tài liệu AI
from fastapi import UploadFile
import logging
from typing import Dict, Any

class DocumentClassifier:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Từ khóa tiếng Việt cho phân loại
        self.document_types = {
            "hóa_đơn": ["hóa đơn", "invoice", "bill", "thanh toán", "payment", "mua hàng"],
            "hợp_đồng": ["hợp đồng", "contract", "agreement", "thỏa thuận", "ký kết"],
            "biên_lai": ["biên lai", "receipt", "phiếu thu", "phiếu chi", "thu tiền"],
            "báo_cáo": ["báo cáo", "report", "statement", "tổng kết", "kết quả"],
            "chứng_từ": ["chứng từ", "voucher", "coupon", "phiếu", "giấy tờ"],
            "khác": ["khác", "other", "unknown"]
        }
    
    async def classify_document(self, file: UploadFile, ocr_text: str = "") -> Dict[str, Any]:
        """Phân loại tài liệu AI - Phiên bản tiếng Việt"""
        try:
            filename_lower = file.filename.lower()
            text_lower = ocr_text.lower()
            
            # Tính điểm cho từng loại
            scores = {doc_type: 0 for doc_type in self.document_types}
            
            # Phân tích dựa trên từ khóa
            for doc_type, keywords in self.document_types.items():
                for keyword in keywords:
                    if keyword in filename_lower:
                        scores[doc_type] += 3  # Ưu tiên tên file
                    if ocr_text and keyword in text_lower:
                        scores[doc_type] += 1  # Nội dung OCR
            
            # Xác định loại có điểm cao nhất
            predicted_type = max(scores, key=scores.get)
            max_score = max(scores.values())
            total_possible = len(keywords) * 4  # Normalize
            
            confidence = max_score / total_possible if total_possible > 0 else 0.1
            confidence = min(confidence, 1.0)  # Giới hạn max 100%
            
            return {
                "loại_tài_liệu": predicted_type,
                "độ_tin_cậy": round(confidence, 2),
                "điểm_số": scores,
                "phương_pháp": "ai_phân_loại_v1",
                "ngôn_ngữ": "vi"
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi phân loại: {e}")
            return {
                "loại_tài_liệu": "khác",
                "độ_tin_cậy": 0.1,
                "lỗi": str(e),
                "phương_pháp": "dự_phòng"
            }

# Instance toàn cục
classifier = DocumentClassifier()
