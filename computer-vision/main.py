import os
from proto.triton_client import TritonClient
from dotenv import load_dotenv
from proto.grpc_server import GrpcServer

load_dotenv()
COMPUTER_VISION_CONTAINER_HOST = os.environ.get("COMPUTER_VISION_CONTAINER_HOST")
TRITON_GRPC_PORT = os.environ.get("TRITON_GRPC_PORT")
COMPUTER_VISION_PORT = os.environ.get("COMPUTER_VISION_PORT")
TRITON_SERVICE = os.environ.get("TRITON_SERVICE")

triton_client = TritonClient(TRITON_SERVICE, TRITON_GRPC_PORT)
server = GrpcServer(triton_client)


def main():
    server.run(COMPUTER_VISION_CONTAINER_HOST, COMPUTER_VISION_PORT)


if __name__ == "__main__":
    main()
