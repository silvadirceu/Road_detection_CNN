import logging
import grpc
from abstractions.http_handler import HttpHandler
from proto import requests_pb2
from proto import requests_pb2_grpc

MAX_MESSAGE_LENGTH = 200 * 1024 * 1024
GRPC_CV_ERROR = "Failed to connect to computer-vision module using grpc"

class GrpcClient(HttpHandler):
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
        self.stub_image = requests_pb2_grpc.ImagePredictServiceStub(self.channel)
        self.stub_video = requests_pb2_grpc.VideoPredictServiceStub(self.channel)

    def send(self, chunk: bytes, file_format: str):
        if file_format in ["mp4", "avi"]:
            return self.__send_video(chunk)
        elif file_format in ["png", "jpg"]:
            return self.__send_image(chunk)
    
    def __send_image(self, chunk: bytes):
        message = requests_pb2.FileRequest(chunk=chunk)
        response = None
        try:
            response: requests_pb2.ImagePredictResponse = self.stub_image.Predict(message)
            print(response)
        except grpc.RpcError as e:
            print(f"gRPC error: code={e.code()} message={e.details()}")
        return response

    def __send_video(self, chunk: bytes):
        message = requests_pb2.FileRequest(chunk=chunk)
        response = None
        try:
            response:requests_pb2.VideoPredictResponse = self.stub_video.Predict(message)
            print(response)
        except grpc.RpcError as e:
            print(f"Received unknown RPC error: code={e.code()} message={e.details()}")
        
        return response
