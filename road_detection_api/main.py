import cv2
from fastapi import FastAPI
import numpy as np
from api.config import PREDICT_PATH
from api.controllers.road_detection_controller import classify_road_condition


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "api is running"}


@app.post("/predict")
async def predict(filename: str, format: str):
    filename_format = f"{filename}.{format}"
    path = str(PREDICT_PATH / filename_format)
    image = cv2.imread(path)

    return classify_road_condition(img=np.array(image))
