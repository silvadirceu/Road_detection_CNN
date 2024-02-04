from dataclasses import dataclass
from models.location.gps_coordinates import GPSCoordinates


@dataclass
class Geolocation(GPSCoordinates):
    street: float