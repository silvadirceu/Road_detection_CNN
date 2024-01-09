import base64
from concurrent import futures
import io
import grpc
import numpy as np
from api.controllers.road_detection_controller import classify_road_condition
from PIL import Image
import proto.file_upload_pb2 as file_upload_pb2
import proto.file_upload_pb2_grpc as file_upload_pb2_grpc


class GrpcServer():
    def __init__(self):
        pass

    class __UploadFileService(file_upload_pb2_grpc.FileUploadServiceServicer):
        def __init__(self):
            self.request = None

        def SendFile(self, request, context):
            file = request.file
            base64_decoded = base64.b64decode(file)
            image = Image.open(io.BytesIO(base64_decoded))
            image = np.array(image)
            prediction = classify_road_condition(img=image)
            result = file_upload_pb2.FileUploadResponse(
                classification=prediction.predicted_category, details=prediction.info
            )
            return result

    def run(self, host="localhost", port="50051", max_workers=10):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
        file_upload_pb2_grpc.add_FileUploadServiceServicer_to_server(
            self.__UploadFileService(), server
        )
        server.add_insecure_port(f"{host}:{port}")
        server.start()
        server.wait_for_termination()
