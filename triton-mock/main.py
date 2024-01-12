import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from proto.grpc_server import GrpcServer

load_dotenv()
GRPC_HOST = os.environ.get("GRPC_HOST")
GRPC_TRITON_PORT = os.environ.get("GRPC_TRITON_PORT")

grpc_server = GrpcServer()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "api is running"}


if __name__ == "__main__":
    grpc_server.run(host=GRPC_HOST, port=GRPC_TRITON_PORT)
    # print("RestAPI initiated at port 8000")
    # uvicorn.run(app, host="0.0.0.0", port=8000)
