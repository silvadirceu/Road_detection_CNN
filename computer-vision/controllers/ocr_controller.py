import grpc
from abstractions.http_client import HttpClient
from proto import requests_pb2
from proto import requests_pb2_grpc

MAX_MESSAGE_LENGTH = 200 * 1024 * 1024


class OcrController(HttpClient):
    def __init__(self, host="localhost", port="50051"):
        options = [
            ("grpc.max_send_message_length", MAX_MESSAGE_LENGTH),
            ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
        ]
        self.host = host
        self.server_port = port
        self.channel = grpc.insecure_channel(
            "{}:{}".format(host, port), options=options
        )
        self.stub_service = requests_pb2_grpc.ImageDataOcrServiceStub(self.channel)

    def send(self, chunk: bytes) -> requests_pb2.ImageDataOCrResponse:
        message = requests_pb2.FileRequest(chunk=chunk)
        response = self.stub_service.Predict(message)
        return response
