from paddleocr import PaddleOCR
from paddle_ocr.paddle_ocr import PaddleOcr
from services.ocr_service import OcrService

road_detection = OcrService(PaddleOcr(
    PaddleOCR(lang="en", use_angle_cls=True, use_gpu=False, show_log=False)
))
