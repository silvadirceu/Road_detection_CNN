from dataclasses import dataclass
from typing import List
import numpy as np
from abstractions.ocr import OpticalCharacterRecognition
from paddle_ocr.paddle_result import PaddleResult
import re


@dataclass
class RoadImageInfo:
    datetime: "PaddleResult" = PaddleResult()
    latitude: "PaddleResult" = PaddleResult()
    longitude: "PaddleResult" = PaddleResult()
    speed: "PaddleResult" = PaddleResult()


class OcrService:
    def __init__(self, ocr: OpticalCharacterRecognition):
        self.__ocr = ocr
        self.__result = RoadImageInfo()

    def __datetime_match(self, text: str, prob: float, pos: List[List]):
        result = None
        pattern = r"(\d{2}-\d{2}-\d{4}) (\d{2})(\d{2})(\d{2})"
        matches = re.search(pattern, text)
        if matches:
            date = matches.group(1)
            hour = matches.group(2)
            minute = matches.group(3)
            second = matches.group(4)
            result = PaddleResult(
                {"date": date, "hour": hour, "minute": minute, "second": second},
                prob,
                pos,
            )
        return result

    def __latitude_match(self, text: str, prob: float, pos: List[List]):
        result = None
        pattern = r"^LAT([-]?\d+\.\d+)[-\s+]?([SWNE])$"
        matches = re.search(pattern, text)

        if matches:
            value = matches.group(1)
            direction = matches.group(2)
            result = PaddleResult(
                {"latitude": value, "direction": direction}, prob, pos
            )
        return result

    def __longitude_match(self, text: str, prob: float, pos: List[List]):
        result = None
        pattern = r"^LON([-]?\d+\.\d+)[-\s+]?([SWNE])$"
        matches = re.search(pattern, text)
        if matches:
            value = matches.group(1)
            direction = matches.group(2)
            result = PaddleResult(
                {"longitude": value, "direction": direction}, prob, pos
            )
        return result

    def __speed_match(self, text: str, prob: float, pos: List[List]):
        result = None
        pattern = r"[sS][pP][eE][eE][dD](\d+\.\d+?)Km/h"
        matches = re.search(pattern, text)
        if matches:
            value = matches.group(1)
            result = PaddleResult({"speed": value}, prob, pos)
        return result

    def __predict_upper_right(self, img:np.ndarray):
        img = img[:int(img.shape[0]*0.25), int(img.shape[1]*0.5):, :]
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
        img = img[int(img.shape[0]*0.25):, int(img.shape[1]*0.5):, :]
        predictions = self.__ocr.predict(img)
        for pred in predictions:
            if pred:
                pos = pred[0][0]
                value = pred[1][0]
                prob = pred[1][1]
                text = re.sub(":", "", value)
                text = re.sub("YY", "W", text)
                #print(text)
                latitude = self.__latitude_match(text, prob, pos)
                if latitude:
                    self.__result.latitude = latitude
                longitude = self.__longitude_match(text, prob, pos)
                if longitude:
                    self.__result.longitude = longitude
                speed = self.__speed_match(text, prob, pos)
                if speed:
                    self.__result.speed = speed


    def predict(self, img: np.ndarray):
        self.__predict_upper_right(img)
        self.__predict_bottom_down(img)
        return self.__result
