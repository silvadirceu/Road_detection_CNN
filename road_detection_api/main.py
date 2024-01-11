from fastapi import FastAPI
import uvicorn
from proto.grpc_server import GrpcServer


grpc_server = GrpcServer()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "api is running"}


if __name__ == "__main__":
    grpc_server.run(host="0.0.0.0", port="8000")
    # print("RestAPI initiated at port 8000")
    # uvicorn.run(app, host="0.0.0.0", port=8000)
