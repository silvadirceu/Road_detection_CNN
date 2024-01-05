from numpy import ndarray
from api.models.road_detection_response import RoadDetectionResponse
from engine.cnn.road_detection_model import RoadDetectionModel
from skimage.io import imread

rdm = RoadDetectionModel()

def classify_road_condition(img: ndarray = None, img_path: str = None):
    if img_path is not None and img is None:
        img = imread(img_path)

    result = rdm.predict(img)

    map_result = {
        "clean": "The road is clean and well-maintained.",
        "dirty": "The road is dirty and may need cleaning.",
        "potholes": "The road contains potholes and needs repair.",
    }

    return RoadDetectionResponse(result, map_result[result])
