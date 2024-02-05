import numpy as np
from paddleocr import PaddleOCR


class PaddleService:
    def __init__(self, paddle_ocr: PaddleOCR):
        self.__paddle_ocr = paddle_ocr

    def predict(self, img: np.ndarray):
        return self.__paddle_ocr.ocr(img)
