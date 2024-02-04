import os

from dotenv import load_dotenv
from proto.grpc_server import GrpcServer
from services.ocr_service import OcrService
from dependency_injector import containers, providers
from ocr.paddle import Paddle


class Container(containers.DeclarativeContainer):
    env_path = os.path.join(
        os.path.abspath(os.path.join(os.getcwd(), os.pardir)), ".env"
    )
    load_dotenv(env_path)

    config = providers.Configuration()
    config.ocr_host.from_env("OCR_CONTAINER_HOST")
    config.ocr_port.from_env("OCR_PORT")

    ocr = providers.Factory(Paddle)

    ocr_service = providers.Factory(
        OcrService,
        ocr=ocr,
    )

    grpc_server = providers.Singleton(GrpcServer, ocr_service=ocr_service)
