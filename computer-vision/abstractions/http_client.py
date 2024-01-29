import abc
from typing import Any


class HttpClient(abc.ABC):
    @abc.abstractmethod
    def send(self, chunk: bytes):
        pass
