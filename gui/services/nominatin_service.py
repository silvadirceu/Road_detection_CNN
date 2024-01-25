from abstractions.geolocator import Geolocator

class NominatinService(Geolocator):
    def __init__(self, geolocator):
        self.geolocator = geolocator

    def adress(self, latitude: float, longitude: float) -> str:
        location = self.geolocator.reverse(f"{latitude}, {longitude}")
        return location.address