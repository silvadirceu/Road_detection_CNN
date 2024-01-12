from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Hole:
    area: str
    location: {"h": str, "w": str}


@dataclass
class RoadDetectionResponse:
    predicted_category: str
    info: str
    #geo_location: Optional[dict] = {"lat": str, "long": str}
    #holes: List[Hole] = []
    #garbage: bool = False
    #marks: bool = False
    #curb: bool = False  # meio fio
    #crosswalk: bool = False
    #timestamp: int
