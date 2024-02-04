from dataclasses import dataclass
from typing import List
from models.road_attr.curb import Curb
from models.road_attr.crack import Crack
from models.road_attr.dirty import Dirty
from models.road_attr.pothole import Pothole
from models.road_attr.traffic_sign import TrafficSign


@dataclass
class RoadAttr:
    potholes: List[Pothole]
    curbs: List[Curb]
    cracks: List[Crack]
    dirty: List[Dirty]
    signs = List[TrafficSign]