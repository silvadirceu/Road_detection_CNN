import abc


class HttpHandler(abc.ABC):
    @abc.abstractmethod
    def send(self, chunk: bytes):
        pass
