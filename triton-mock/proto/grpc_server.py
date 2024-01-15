from concurrent import futures
import grpc
from controllers.road_detection_controller import classify_road_condition
from utils.serializers import bytes_to_ndarray
from proto import file_upload_pb2
from proto import file_upload_pb2_grpc


MAX_MESSAGE_LENGTH = 200 * 1024 * 1024


class GrpcServer:
    def __init__(self):
        pass

    class __TritonPredictService(file_upload_pb2_grpc.TritonPredictServiceServicer):
        def __init__(self):
            pass

        def TritonPredict(self, request:file_upload_pb2.TritonPredictRequest, context):
            prediction = classify_road_condition(img=bytes_to_ndarray(request.chunk))
            result = file_upload_pb2.TritonPredictResponse(classification=prediction.predicted_category, details=prediction.info)
            return result

    def run(self, host="localhost", port="50051", max_workers=10):
        options = [
            ("grpc.max_send_message_length", MAX_MESSAGE_LENGTH),
            ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
        ]
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers), options=options
        )
        file_upload_pb2_grpc.add_TritonPredictServiceServicer_to_server(
            self.__TritonPredictService(), server
        )
        server.add_insecure_port(f"{host}:{port}")
        server.start()
        print(
            f"gRPC Server running at {host}:{port}",
        )
        server.wait_for_termination()
