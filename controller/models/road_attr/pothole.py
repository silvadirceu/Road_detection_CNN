from dataclasses import dataclass
from models.location.gps_coordinates import GPSCoordinates


@dataclass
class Pothole(GPSCoordinates):
    area: float = 0
    depth: float = 0