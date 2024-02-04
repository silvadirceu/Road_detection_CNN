import numpy as np
from abstractions.ocr import Ocr


class Ocr(Ocr):
    def __init__(self, ocr):
        self.__ocr = self.ocr

    def predict(self, img: np.ndarray):
        return self.__ocr.ocr(img)
