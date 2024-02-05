from abstractions.controllers.grpc_client_controller import GrpcClientController
from abstractions.http_client import HttpClient
from proto import requests_pb2
from proto import requests_pb2_grpc

MAX_MESSAGE_LENGTH = 200 * 1024 * 1024

class ComputerVisionController(GrpcClientController):
    def send(self, chunk: bytes):
        message = requests_pb2.FileRequest(chunk=chunk)
        response: requests_pb2.RoadVideoDataResponse = self.stub.GetVideoData(message)
        return response