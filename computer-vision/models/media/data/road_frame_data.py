
from dataclasses import dataclass
from uuid import UUID
from models.road_attr.road_attr import RoadAttr
from models.location.gps_coordinates import GPSCoordinates


@dataclass
class RoadFrameData:
    id: int
    video_id: UUID
    video_time: float
    datetime: str
    speed: float
    geoposition: GPSCoordinates
    attributes: RoadAttr
    image: str