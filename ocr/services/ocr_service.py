from datetime import timedelta, datetime
from typing import List
import numpy as np
from models.inference_result import InferenceResult
import re
from models.road_image_info import RoadImageInfo
from services.paddle_service import PaddleService

class OcrService:
    def __init__(self, paddle_service: PaddleService):
        self.__ocr = paddle_service
        self.__result = RoadImageInfo()

    def __datetime_match(self, text: str, prob: float, pos: List[List]):
        result = InferenceResult()
        pattern = r"(\d{2}-\d{2}-\d{4}) (\d{2})(\d{2})(\d{2})"
        matches = re.search(pattern, text)
        if matches:
            date = matches.group(1)
            hour = matches.group(2)
            minute = matches.group(3)
            second = matches.group(4)
            result = InferenceResult(
                f"{date} {hour}:{minute}:{second}",
                prob,
                pos,
            )
        return result

    def __latitude_match(self, text: str, prob: float, pos: List[List]):
        result = InferenceResult()
        pattern = r"^LAT([-]?\d+\.\d+)[-\s+]?([SWNE])$"
        matches = re.search(pattern, text)

        if matches:
            value = matches.group(1)
            direction = matches.group(2)
            result = InferenceResult(
                f"{value} {direction}", prob, pos
            )
        return result

    def __longitude_match(self, text: str, prob: float, pos: List[List]):
        result = InferenceResult()
        pattern = r"^LON([-]?\d+\.\d+)[-\s+]?([SWNE])$"
        matches = re.search(pattern, text)
        if matches:
            value = matches.group(1)
            direction = matches.group(2)
            result = InferenceResult(
                f"{value} {direction}", prob, pos
            )
        return result

    def __speed_match(self, text: str, prob: float, pos: List[List]):
        result = InferenceResult()
        pattern = r"[sS][pP][eE][eE][dD](\d+\.\d+?)Km/h"
        matches = re.search(pattern, text)
        if matches:
            value = matches.group(1)
            result = InferenceResult(value, prob, pos)
        return result

    def __predict_upper_right(self, img: np.ndarray):
        img = img[: int(img.shape[0] * 0.25), int(img.shape[1] * 0.5) :, :]
        pred = self.__ocr.predict(img)
        if pred:
            pred = pred[0]
            pos = pred[0][0]
            value = pred[1][0]
            prob = pred[1][1]
            text = re.sub(":", "", value)
            datetime = self.__datetime_match(text, prob, pos)
            if datetime:
                self.__result.datetime = self.__datetime_match(text, prob, pos)

    def __predict_bottom_down(self, img: np.ndarray):
        img = img[int(img.shape[0] * 0.25) :, int(img.shape[1] * 0.5) :, :]
        predictions = self.__ocr.predict(img)
        for pred in predictions:
            if pred:
                pos = pred[0][0]
                value = pred[1][0]
                prob = pred[1][1]
                text = re.sub(":", "", value)
                text = re.sub("YY", "W", text)
                latitude = self.__latitude_match(text, prob, pos)
                if latitude.value:
                    self.__result.latitude = latitude
                longitude = self.__longitude_match(text, prob, pos)
                if longitude.value:
                    self.__result.longitude = longitude
                speed = self.__speed_match(text, prob, pos)
                if speed.value:
                    self.__result.speed = speed

    def predict(self, img: np.ndarray):
        self.__predict_upper_right(img)
        self.__predict_bottom_down(img)
        return self.__result
