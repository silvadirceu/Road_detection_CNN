import os
from handlers.camera_handler import CameraHandler
from proto.grpc_client import GrpcClient
from dotenv import load_dotenv

load_dotenv()
CV_CONTAINER = os.environ.get("CV_CONTAINER")
GRPC_CV_PORT = os.environ.get("GRPC_CV_PORT")
CAMERA_CONNECTION_STRING = os.environ.get("CAMERA_CONNECTION_STRING")

cv_client = GrpcClient(CV_CONTAINER, GRPC_CV_PORT)
cam = CameraHandler(cv_client, CAMERA_CONNECTION_STRING)


def main():
    cam.send_video_parallel()


if __name__ == "__main__":
    main()
