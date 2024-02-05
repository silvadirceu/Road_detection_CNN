import logging
import os

from dotenv import load_dotenv
from paddleocr import PaddleOCR
from controllers.api_controller import ApiController
from services.ocr_service import OcrService
from dependency_injector import containers, providers

from services.paddle_service import PaddleService


class Container(containers.DeclarativeContainer):
    env_path = os.path.join(
        os.path.abspath(os.path.join(os.getcwd(), os.pardir)), ".env"
    )
    load_dotenv(env_path)

    config = providers.Configuration()
    config.ocr_host.from_env("OCR_CONTAINER_HOST")
    config.ocr_port.from_env("OCR_PORT")

    paddle_ocr = providers.Factory(
        PaddleOCR, lang="en", use_angle_cls=True, use_gpu=False, show_log=False
    )

    paddle_service = providers.Factory(PaddleService, paddle_ocr=paddle_ocr)

    ocr_service = providers.Factory(
        OcrService,
        paddle_service=paddle_service,
    )

    server = providers.Singleton(ApiController, ocr_service=ocr_service)
