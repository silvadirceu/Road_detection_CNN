import os
from models.media.data.road_video_data import RoadVideoData
from controllers.ocr_controller import OcrController
from controllers.triton_controller import TritonController
from dotenv import load_dotenv
from controllers.api_controller import ApiController

load_dotenv()
COMPUTER_VISION_CONTAINER_HOST = os.environ.get("COMPUTER_VISION_CONTAINER_HOST")
TRITON_GRPC_PORT = os.environ.get("TRITON_GRPC_PORT")
COMPUTER_VISION_PORT = os.environ.get("COMPUTER_VISION_PORT")
TRITON_SERVICE = os.environ.get("TRITON_SERVICE")
OCR_SERVICE = os.environ.get("OCR_SERVICE")
OCR_PORT = os.environ.get("OCR_PORT")


triton_client = TritonController(TRITON_SERVICE, TRITON_GRPC_PORT)
ocr_client = OcrController(OCR_SERVICE, OCR_PORT)
server = ApiController(triton_client, ocr_client)


def main():
    server.run(COMPUTER_VISION_CONTAINER_HOST, COMPUTER_VISION_PORT)


if __name__ == "__main__":
    main()
