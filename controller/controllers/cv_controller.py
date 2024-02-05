from abstractions.controllers.grpc_client_controller import GrpcClientController
from proto import requests_pb2
from proto.requests_pb2_grpc import RoadVideoDataServiceStub

class ComputerVisionController(GrpcClientController):
    def __typing__(self):
        self.stub: RoadVideoDataServiceStub

    def send(self, chunk: bytes):
        message = requests_pb2.FileRequest(chunk=chunk)
        response: requests_pb2.RoadVideoDataResponse = self.stub.GetVideoData(message)
        return response
