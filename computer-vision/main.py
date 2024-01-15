import os
from proto.triton_client import TritonClient
from dotenv import load_dotenv
from proto.grpc_server import GrpcServer

load_dotenv()
GRPC_HOST = os.environ.get("GRPC_HOST")
GRPC_TRITON_PORT = os.environ.get("GRPC_TRITON_PORT")
GRPC_CV_PORT = os.environ.get("GRPC_CV_PORT")
CAMERA_CONNECTION_STRING = os.environ.get("CAMERA_CONNECTION_STRING")
TRITON_CONTAINER = os.environ.get("TRITON_CONTAINER")

triton_client = TritonClient(TRITON_CONTAINER, GRPC_TRITON_PORT)
server = GrpcServer(triton_client)


def main():
    server.run(GRPC_HOST, GRPC_CV_PORT)


if __name__ == "__main__":
    main()
