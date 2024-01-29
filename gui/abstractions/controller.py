import abc

from abstractions.http_handler import HttpHandler


class Controller(abc.ABC):
    @abc.abstractmethod
    def __init__(self, http_handler: HttpHandler):
        pass
