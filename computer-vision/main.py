import os
from proto.triton_client import TritonClient
from dotenv import load_dotenv
from proto.grpc_server import GrpcServer

load_dotenv()
GRPC_HOST = os.environ.get("GRPC_HOST") or "0.0.0.0"
GRPC_TRITON_PORT = os.environ.get("GRPC_TRITON_PORT") or "8001"
GRPC_CV_PORT = os.environ.get("GRPC_CV_PORT") or "8080"
TRITON_CONTAINER = os.environ.get("TRITON_CONTAINER") or "triton-server"

triton_client = TritonClient(TRITON_CONTAINER, GRPC_TRITON_PORT)
server = GrpcServer(triton_client)


def main():
    server.run(GRPC_HOST, GRPC_CV_PORT)


if __name__ == "__main__":
    main()
