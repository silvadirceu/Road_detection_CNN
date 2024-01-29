import os
from handlers.camera_handler import CameraHandler
from proto.grpc_client import GrpcClient
from dotenv import load_dotenv

load_dotenv()
COMPUTER_VISION_SERVICE = os.environ.get("COMPUTER_VISION_SERVICE") or "computer-vision"
COMPUTER_VISION_PORT = os.environ.get("COMPUTER_VISION_PORT") or "80"
CAMERA_CONNECTION_STRING = os.environ.get("CAMERA_CONNECTION_STRING")

cv_client = GrpcClient(COMPUTER_VISION_SERVICE, COMPUTER_VISION_PORT)
cam = CameraHandler(cv_client, CAMERA_CONNECTION_STRING)


def main():
    cam.send_video_parallel()


if __name__ == "__main__":
    main()
