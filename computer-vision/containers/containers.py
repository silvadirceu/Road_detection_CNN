import os
from dotenv import load_dotenv
from controllers.api_controller import ApiController
from dependency_injector import containers, providers
from controllers.ocr_controller import OcrController
from controllers.triton_controller import TritonController


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

    triton_controller = providers.Singleton(TritonController, config.triton_service(),  config.triton_grpc_port())
    ocr_controller =  providers.Singleton(OcrController, config.ocr_service(),  config.ocr_grpc_port())
    server = providers.Singleton(ApiController, triton_controller, ocr_controller)