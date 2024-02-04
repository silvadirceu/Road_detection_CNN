from dataclasses import dataclass
from models.inference_result import InferenceResult


@dataclass
class RoadImageInfo:
    datetime: "InferenceResult" = InferenceResult()
    latitude: "InferenceResult" = InferenceResult()
    longitude: "InferenceResult" = InferenceResult()
    speed: "InferenceResult" = InferenceResult()

