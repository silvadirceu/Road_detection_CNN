# Deploying a TensorFlow Model

This README demonstrates how to deploy a simple model on Triton Inference Server.

## Step 1: Export the Model

Export the TensorFlow model as a saved_model. This can be done using the `keras.models.save_model` function.

## Step 2: Set Up Triton Inference Server

To use Triton, you need to build a model repository. The structure of the repository should be as follows:

```
model_repository
|
+-- model_name
    |
    +-- config.pbtxt
    +-- 1
        |
        +-- model.savedmodel
            |
            +-- saved_model.pb
            +-- variables
                |
                +-- variables.data-00000-of-00001
                +-- variables.index
```

### Step 2.1: Configuring the config.pbtxt file

Here's an example of how the config.pbtxt file in this repository is configured:

```plaintext
name: "road_detection_cnn"
platform: "tensorflow_savedmodel"
max_batch_size : 0
input [
  {
    name: "conv2d_input"
    data_type: TYPE_FP32
    dims: [-1, 150, 150, 1]
  }
]
output [
  {
    name: "dense_1"
    data_type: TYPE_FP32
    dims: [-1, 3]
  }
]
```

### Step 2.2: Run the container
Run the container
For GPU:

```bash
docker run --gpus all --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 -v ${PWD}/model_repository:/models nvcr.io/nvidia/tritonserver:<xx.yy>-py3 tritonserver --model-repository=/models --backend-config=tensorflow,version=2
```

Without GPU:

```bash
docker run --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 -v ${PWD}/model_repository:/models nvcr.io/nvidia/tritonserver:<xx.yy>-py3 tritonserver --model-repository=/models --backend-config=tensorflow,version=2
```

## Step 3: Using the Triton Client

Install dependencies & download an example image to test inference.

```bash
pip install tritonclient[grpc]
```

First, import all the necessary libraries.

```python
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput
```

Establish a connection to the Triton server's gRPC endpoint.

```python
InferenceServerClient(url=f"{host}:{port}")
```

Specify the input: input name, shape, and data type.

```python
inputs = InferInput("conv2d_input", img_resized.shape, datatype="FP32")
inputs.set_data_from_numpy(img_resized)
```

For the output, specify the name and the number of classes.

```python
output = InferRequestedOutput("dense_1", class_count=3)
```

The response will be in the following format:

```python
response = self.__triton_client.infer(model_name="road_detection_cnn", inputs=[inputs], outputs=[output])
result = response.as_numpy("dense_1")
print(result)
```

For a practical example, refer to the file:

```plaintext
computer-vision/triton_client.py
```

The output is in the format: `<confidence_score>:<classification_index>`.

## Official Documentation:
- [Triton Inference Server Quick Deploy Tutorial](https://github.com/triton-inference-server/tutorials/blob/main/Quick_Deploy/TensorFlow/README.md)
