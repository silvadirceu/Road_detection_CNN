import os
from time import sleep
from abstractions.http_handler import HttpHandler
from handlers.camera_handler import CameraHandler
from proto.grpc_client import GrpcClient
from dotenv import load_dotenv

load_dotenv()
GRPC_HOST = os.environ.get("GRPC_HOST")
GRPC_CV_PORT = os.environ.get("GRPC_CV_PORT")
CAMERA_CONNECTION_STRING = os.environ.get("CAMERA_CONNECTION_STRING")

grpc_cv_client: HttpHandler = GrpcClient(host=GRPC_HOST, port=GRPC_CV_PORT)
cam_handler = CameraHandler(grpc_cv_client, CAMERA_CONNECTION_STRING)


def main():
    cam_handler.send_video_parallel()
    while True:
        print("Running other parts of the code.")
        sleep(2)


if __name__ == "__main__":
    main()
