from concurrent import futures
from io import BytesIO
import pickle
import grpc
from grpc import ServicerContext
from abstractions.http_client import HttpClient
from abstractions.http_server import HttpServer
from proto import requests_pb2_grpc
from controllers.ocr_controller import OcrController
from proto.requests_pb2 import (
    TritonPredictResponse,
    FileRequest,
    ImagePredictResponse,
    VideoPredictResponse,
)
from controllers.triton_controller import TritonController
from utils.file import FileInfo, video2image
from utils.image import Image, ImageUtils

MAX_MESSAGE_LENGTH = 200 * 1024 * 1024


class ApiController(HttpServer):
    def __init__(self, triton_controller: HttpClient, ocr_controller: OcrController):
        self.triton_client = triton_controller
        self.ocr_client = ocr_controller

    class __ImagePredictService(requests_pb2_grpc.ImagePredictServiceServicer):
        def __init__(self, triton_client: TritonController, ocr_client: OcrController):
            self.triton_client = triton_client
            self.ocr_client = ocr_client

        def Predict(self, request: FileRequest, context: ServicerContext):
            img_array = ImageUtils.to_nddaray(request.chunk)
            ocr_response = self.ocr_client.send(pickle.dumps(img_array))
            triton_grpc_response = self.triton_client.send(pickle.dumps(img_array))
            triton_response = TritonPredictResponse(
                classification=triton_grpc_response,
                frame_time="0",
                latitude=ocr_response.latitude,
                longitude=ocr_response.longitude,
            )
            response = ImagePredictResponse(prediction=triton_response)
            return response

    class __VideoPredictService(requests_pb2_grpc.VideoPredictServiceServicer):
        def __init__(self, triton_client: TritonController, ocr_client: OcrController):
            self.triton_client = triton_client
            self.ocr_client = ocr_client

        def Predict(self, request: FileRequest, context: ServicerContext):
            file_info = FileInfo("dump", request.chunk)
            frames_generator = ImageUtils.to_frame(file_info)
            predictions = []
            for frame_array, frame_time in frames_generator:
                frame_byte = pickle.dumps(frame_array)
                ocr_response = self.ocr_client.send(frame_byte)
                triton_grpc_response = self.triton_client.send(frame_byte)
                triton_response = TritonPredictResponse(
                    classification=triton_grpc_response,
                    frame_time=str(frame_time),
                    latitude=ocr_response.latitude,
                    longitude=ocr_response.longitude,
                )
                predictions.append(triton_response)
            response = VideoPredictResponse(predictions=predictions)
            return response

    def run(self, host="localhost", port="50051", max_workers=10):
        options = [
            ("grpc.max_send_message_length", MAX_MESSAGE_LENGTH),
            ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
        ]
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers), options=options
        )

        requests_pb2_grpc.add_ImagePredictServiceServicer_to_server(
            self.__ImagePredictService(self.triton_client, self.ocr_client), server
        )
        requests_pb2_grpc.add_VideoPredictServiceServicer_to_server(
            self.__VideoPredictService(self.triton_client, self.ocr_client), server
        )

        server.add_insecure_port(f"{host}:{port}")
        server.start()
        print(
            f"gRPC Server running at {host}:{port}",
        )
        server.wait_for_termination()
