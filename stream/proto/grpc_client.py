import grpc
from abstractions.http_client import HttpClient
import proto.file_upload_pb2_grpc as file_upload_pb2_grpc
import proto.file_upload_pb2 as file_upload_pb2

MAX_MESSAGE_LENGTH = 200 * 1024 * 1024


class GrpcClient(HttpClient):
    def __init__(self, host="localhost", port="50051"):
        options = [
            ("grpc.max_send_message_length", MAX_MESSAGE_LENGTH),
            ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
        ]
        self.host = host
        self.server_port = port
        self.channel = grpc.insecure_channel(
            "{}:{}".format(self.host, self.server_port), options=options
        )
        self.stub = file_upload_pb2_grpc.UploadImageServiceStub(self.channel)

    def send(self, chunk: bytes) -> file_upload_pb2.UploadImageResponse:
        message = file_upload_pb2.UploadImageRequest(chunk=chunk)
        response = self.stub.UploadImage(message)
        return response
