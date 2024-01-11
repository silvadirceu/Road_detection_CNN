import os
from abstractions.http_handler import HttpHandler
from proto.triton_client import TritonClient
from dotenv import load_dotenv

from proto.grpc_server import GrpcServer

load_dotenv()
GRPC_HOST = os.environ.get("GRPC_HOST")
GRPC_CONTROLLER_PORT = os.environ.get("GRPC_TRITON_PORT")
GRPC_CV_PORT = os.environ.get("GRPC_CV_PORT")
CAMERA_CONNECTION_STRING = os.environ.get("CAMERA_CONNECTION_STRING")

grpc_triton_client: HttpHandler = TritonClient(host=GRPC_HOST, port=GRPC_CONTROLLER_PORT)
grpc_server = GrpcServer(grpc_triton_client)

def main():
    grpc_server.run("0.0.0.0", GRPC_CV_PORT)
    pass

if __name__ == "__main__":
    main()
