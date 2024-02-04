import abc
from typing import List
import numpy as np


class Ocr(abc.ABC):
    def __init__(self):
        pass

    def predict(self, img: np.ndarray) -> List:
        pass
