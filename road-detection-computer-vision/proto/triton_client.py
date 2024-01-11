import grpc
from abstractions.http_handler import HttpHandler
import proto.file_upload_pb2_grpc as file_upload_pb2_grpc
import proto.file_upload_pb2 as file_upload_pb2

MAX_MESSAGE_LENGTH = 200 * 1024 * 1024


class TritonClient(HttpHandler):
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
        self.stub_predict = file_upload_pb2_grpc.TritonPredictServiceStub(self.channel)

    def send(self, chunk: bytes) -> file_upload_pb2.TritonPredictResponse:
        message = file_upload_pb2.TritonPredictRequest(chunk=chunk)
        response = self.stub_predict.TritonPredict(message)
        return response
