import abc


class GrpcServerController(abc.ABC):
    @abc.abstractclassmethod
    def run():
        pass
