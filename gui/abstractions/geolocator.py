import abc


class Geolocator(abc.ABC):
    @abc.abstractmethod
    def __init__(self, geolocator):
        self.__geolocator = geolocator

    @abc.abstractmethod
    def adress(self, latitude: float, longitude: float):
        pass
