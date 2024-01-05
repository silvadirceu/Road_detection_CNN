
from dataclasses import dataclass


@dataclass
class RoadDetectionResponse:
    predicted_category: str
    info: str