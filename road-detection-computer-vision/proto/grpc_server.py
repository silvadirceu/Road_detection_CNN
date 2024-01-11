from concurrent import futures
import grpc
from grpc import ServicerContext
from handlers.video_handler import VideoHandler
import proto.file_upload_pb2_grpc as file_upload_pb2_grpc
from proto.file_upload_pb2 import (
    TritonPredictResponse,
    UploadImageRequest,
    UploadVideoRequest,
    UploadImageResponse,
    UploadVideoResponse,
)
from proto.triton_client import TritonClient
from utils.file import FileInfo, image2bytes, video2image

MAX_MESSAGE_LENGTH = 200 * 1024 * 1024


class GrpcServer:
    def __init__(self, triton_client: TritonClient):
        self.triton_client = triton_client
        pass

    class __UploadImageService(file_upload_pb2_grpc.UploadImageServiceServicer):
        def __init__(self,triton_client: TritonClient):
            self.triton_client = triton_client
            pass

        def UploadImage(self, request: UploadImageRequest, context: ServicerContext):
            file_info = FileInfo("test.q", request.chunk)
            img_bytes = image2bytes(file_info)
            response = UploadImageResponse(prediction=self.triton_client.send(img_bytes))
            return response

    class __UploadVideoService(file_upload_pb2_grpc.UploadVideoServiceServicer):
        def __init__(self, triton_client: TritonClient):
            self.triton_client = triton_client
            pass

        def UploadVideo(self, request: UploadVideoRequest, context: ServicerContext):
            file_info = FileInfo("test.q", request.chunk)
            frames_generator = video2image(file_info, 20)
            predictions = []
            for frame_byte in frames_generator:
                predict_result = self.triton_client.send(frame_byte)
                predictions.append(predict_result)
            response = UploadVideoResponse(predictions=predictions)
            return response

    def run(self, host="localhost", port="50051", max_workers=10):
        options = [
            ("grpc.max_send_message_length", MAX_MESSAGE_LENGTH),
            ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
        ]
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers), options=options
        )

        file_upload_pb2_grpc.add_UploadImageServiceServicer_to_server(
            self.__UploadImageService(self.triton_client), server
        )
        file_upload_pb2_grpc.add_UploadVideoServiceServicer_to_server(
            self.__UploadVideoService(self.triton_client), server
        )
        server.add_insecure_port(f"{host}:{port}")
        server.start()
        print(
            f"gRPC Server running at {host}:{port}",
        )
        server.wait_for_termination()
