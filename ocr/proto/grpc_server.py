from concurrent import futures
import logging
import grpc
from grpc import ServicerContext
from abstractions.http_server import HttpServer
from services.ocr_service import OcrService
from proto import requests_pb2_grpc
from proto.requests_pb2 import ImageDataOCrResponse, FileRequest
import pickle


MAX_MESSAGE_LENGTH = 200 * 1024 * 1024


class GrpcServer(HttpServer):
    def __init__(self, ocr_service: OcrService):
        self.__ocr_service = ocr_service

    class __ImageDataService(requests_pb2_grpc.ImageDataOcrServiceServicer):
        def __init__(self, ocr_service: OcrService):
            self.__ocr_service = ocr_service
            pass

        def Predict(self, request: FileRequest, context: ServicerContext):
            pred = self.__ocr_service.predict(pickle.loads(request.chunk))
            date = pred.datetime.value["date"]
            hour = pred.datetime.value["hour"]
            min = pred.datetime.value["minute"]
            sec = pred.datetime.value["second"]

            response = ImageDataOCrResponse(
                latitude=pred.latitude.value["latitude"],
                longitude=pred.longitude.value["longitude"],
                datetime=f"{date} {hour}:{min}:{sec}",
                speed=pred.speed.value["speed"],
            )
            return response

    def run(self, host="localhost", port="50051", max_workers=10):
        options = [
            ("grpc.max_send_message_length", MAX_MESSAGE_LENGTH),
            ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
        ]
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers), options=options
        )

        requests_pb2_grpc.add_ImageDataOcrServiceServicer_to_server(
            self.__ImageDataService(self.__ocr_service), server
        )

        server.add_insecure_port(f"{host}:{port}")
        server.start()
        print(
            f"gRPC Server running at {host}:{port}",
        )
        server.wait_for_termination()
