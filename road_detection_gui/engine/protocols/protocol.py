import abc


class Protocol(abc.ABC):
    @abc.abstractmethod
    def send(self, chunk):
        pass
