import os
from dotenv import load_dotenv
from dependency_injector import containers, providers
from abstractions.controllers.grpc_server_controller import GrpcServerController
from controllers.api_controller import ApiController
from controllers.cv_controller import ComputerVisionController
from proto.requests_pb2_grpc import RoadVideoDataServiceStub


class Container(containers.DeclarativeContainer):
    env_path = os.path.join(
        os.path.abspath(os.path.join(os.getcwd(), os.pardir)), ".env"
    )
    load_dotenv(env_path)

    config = providers.Configuration()
    config.host.from_env("COMPUTER_VISION_CONTAINER_HOST")
    config.port.from_env("COMPUTER_VISION_PORT")
    config.triton_service.from_env("TRITON_SERVICE")
    config.triton_grpc_port.from_env("TRITON_GRPC_PORT")
    config.ocr_service.from_env("OCR_SERVICE")
    config.ocr_grpc_port.from_env("OCR_PORT")

    cv_controller = providers.Factory(
        ComputerVisionController, RoadVideoDataServiceStub
    )
    server: GrpcServerController = ApiController()
