import abc
from typing import Any


class HttpHandler(abc.ABC):
    @abc.abstractmethod
    def send(self, chunk: bytes):
        pass
