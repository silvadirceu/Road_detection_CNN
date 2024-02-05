import abc
import grpc
MAX_MESSAGE_LENGTH = 200 * 1024 * 1024

class GrpcClientController(abc.ABC):
    def __init__(self, stub: object, host="localhost", port="50051"):
        options = [
            ("grpc.max_send_message_length", MAX_MESSAGE_LENGTH),
            ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
        ]
        self.host = host
        self.server_port = port
        self.channel = grpc.insecure_channel(
            "{}:{}".format(self.host, self.server_port), options=options
        )
        self.stub = stub

    @abc.abstractmethod
    def send(self, chunk: bytes):
        pass
    