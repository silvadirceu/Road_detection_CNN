import abc
class HttpServer(abc.ABC):
    @abc.abstractclassmethod
    def run():
        pass
