import grpc
from engine.protocols.protocol import Protocol
from engine.utils.data import bytes_to_base64_utf8encoded
import proto.file_upload_pb2_grpc as file_upload_pb2_grpc
import proto.file_upload_pb2 as file_upload_pb2


class Grpc_Client(Protocol):
    def __init__(self, host = "localhost", port="50051"):
        self.host = host
        self.server_port = port
        self.channel = grpc.insecure_channel(
            "{}:{}".format(self.host, self.server_port)
        )
        self.stub = file_upload_pb2_grpc.FileUploadServiceStub(self.channel)

    def send(self, chunk):
        bytes_encoded = bytes_to_base64_utf8encoded(chunk)
        message = file_upload_pb2.FileUploadRequest(file=bytes_encoded)
        response = self.stub.SendFile(message)
        return response
