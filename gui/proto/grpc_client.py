import grpc
from abstractions.http_handler import HttpHandler
import proto.file_upload_pb2_grpc as file_upload_pb2_grpc
import proto.file_upload_pb2 as file_upload_pb2

MAX_MESSAGE_LENGTH = 200 * 1024 * 1024


class Grpc_Client():
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
    
    def send_image(self, chunk: bytes):
        message = file_upload_pb2.UploadImageRequest(chunk=chunk)
        response = self.stub_image.UploadImage(message)
        return response
    
    def send_video(self, chunk: bytes):
        message = file_upload_pb2.UploadVideoRequest(chunk=chunk)
        response = self.stub_video.UploadVideo(message)
        return response
