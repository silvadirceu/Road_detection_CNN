from concurrent import futures
import grpc
from grpc import ServicerContext
from abstractions.controllers.grpc_server_controller import GrpcServerController, HttpServer
from proto import requests_pb2_grpc
from proto.requests_pb2 import FileRequest, RoadVideoDataResponse
import pickle

MAX_MESSAGE_LENGTH = 200 * 1024 * 1024


class ApiController(GrpcServerController):
    def __init__(self):
        pass

    class __RoadVideoDataService(requests_pb2_grpc.RoadVideoDataServiceServicer):
        def __init__(self):
            pass

        def Predict(self, request: FileRequest, context: ServicerContext):
            pred = self.__ocr_service.predict(pickle.loads(request.chunk))
            response = RoadVideoDataResponse(
                latitude=pred.latitude.value,
                longitude=pred.longitude.value,
                datetime=pred.datetime.value,
                speed=pred.speed.value,
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
            self.__RoadVideoDataService(), server
        )

        server.add_insecure_port(f"{host}:{port}")
        server.start()
        print(
            f"gRPC Server running at {host}:{port}",
        )
        server.wait_for_termination()
