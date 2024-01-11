from pathlib import Path


MODEL_PATH = Path("triton/cnn/ckpt/trained_model.h5")
TRAIN_PATH = Path("road_images/train/")
TEST_PATH = Path("road_images/test/")
CATEGORIES = ["dirty", "potholes", "clean"]
