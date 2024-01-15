import abc


class HttpClient(abc.ABC):
    @abc.abstractmethod
    def send(self, chunk: bytes):
        pass
