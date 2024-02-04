import numpy as np
from paddleocr import PaddleOCR
from abstractions.ocr import Ocr


class Paddle(Ocr):
    def __init__(self):
        self.__ocr = PaddleOCR(lang="en", use_angle_cls=True, use_gpu=False, show_log=False)

    def predict(self, img: np.ndarray):
        return self.__ocr.ocr(img)
