from numpy import ndarray
from engine.cnn.road_detection_model import RoadDetectionModel
from skimage.io import imread


def classify_road_condition(img: ndarray = None, img_path: str = None):
    if img_path is not None and img is None:
        img = imread(img_path)

    rdm = RoadDetectionModel()
    result = rdm.predict(img)

    map_result = {
        "clean": "The road is clean and well-maintained.",
        "dirty": "The road is dirty and may need cleaning.",
        "potholes": "The road contains potholes and needs repair.",
    }

    return {"Result": result, "map_result": map_result[result]}
