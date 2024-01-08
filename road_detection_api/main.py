import base64
import io
from fastapi import FastAPI, Form
import numpy as np
from api.config import PREDICT_PATH
from api.controllers.road_detection_controller import classify_road_condition
from PIL import Image

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "api is running"}

@app.post("/predict")
async def predict(file_base64: str):
    base64_decoded = base64.b64decode(file_base64)
    image = Image.open(io.BytesIO(base64_decoded))
    image = np.array(image)
    return classify_road_condition(img=image)

@app.post("/local/predict")
async def predict(filename: str, format: str):
    filename_format = f"{filename}.{format}"
    filename_path = str(PREDICT_PATH / filename_format)
    return classify_road_condition(img_path=filename_path)
