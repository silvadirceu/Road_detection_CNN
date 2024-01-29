import logging
import grpc
from abstractions.http_handler import HttpHandler
import proto.file_upload_pb2_grpc as file_upload_pb2_grpc
import proto.file_upload_pb2 as file_upload_pb2

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
        self.stub_image = file_upload_pb2_grpc.UploadImageServiceStub(self.channel)
        self.stub_video = file_upload_pb2_grpc.UploadVideoServiceStub(self.channel)

    def send(self, chunk: bytes, file_format: str):
        if file_format in ["mp4", "avi"]:
            return self.__send_video(chunk)
        elif file_format in ["png", "jpg"]:
            return self.__send_image(chunk)
    
    def __send_image(self, chunk: bytes):
        message = file_upload_pb2.UploadImageRequest(chunk=chunk)
        response = None
        try:
            response:file_upload_pb2.UploadImageResponse = self.stub_image.UploadImage(message)
        except:
            logging.error(GRPC_CV_ERROR)
        return response

    def __send_video(self, chunk: bytes):
        message = file_upload_pb2.UploadVideoRequest(chunk=chunk)
        response = None
        try:
            response:file_upload_pb2.UploadVideoResponse = self.stub_video.UploadVideo(message)
        except:
            logging.error(GRPC_CV_ERROR)
        
        return response
