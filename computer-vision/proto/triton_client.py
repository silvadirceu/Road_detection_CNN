import numpy as np
from abstractions.http_client import HttpClient
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput
from skimage.transform import resize
from utils.serializers import bytes_to_ndarray

MAX_MESSAGE_LENGTH = 200 * 1024 * 1024


class TritonClient(HttpClient):
    def __init__(self, host="localhost", port="50051"):
        self.host = host
        self.server_port = port
        self.__triton_client = InferenceServerClient(url=f"{host}:{port}")

    def send(self, chunk: bytes):
        img_array = bytes_to_ndarray(chunk)
        img = resize(img_array, (150, 150, 1))
        img_resized = img.reshape(1, 150, 150, 1)
        img_resized = img_resized.astype(np.float32)
        inputs = InferInput("conv2d_input", img_resized.shape, datatype="FP32")
        inputs.set_data_from_numpy(img_resized)
        output = InferRequestedOutput("dense_1", class_count=3)
        print(f"{self.host}:{self.server_port}")
        response = self.__triton_client.infer(
            model_name="road_detection_cnn", inputs=[inputs], outputs=[output]
        )
        result = response.as_numpy("dense_1")
        result = str(result[0])
        return result.split(":")[-1].replace("'", "")