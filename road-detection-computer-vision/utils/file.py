import cv2
import os
from utils.serializers import ndarray_to_bytes

DIR_OUT_PATH = "data"


class FileInfo:
    def __init__(self, name: str, chunk: bytes, path=""):
        self.name = name
        self.file_type = os.path.basename(self.name).split(".")[-1]
        self.chunk = chunk
        self.path = path


def video2image(file_info: FileInfo, step: int):
    save_uploaded_file(file_info)

    cam = cv2.VideoCapture(os.path.join(DIR_OUT_PATH, file_info.name))
    current_frame = 0
    while True:
        ret, frame = cam.read()
        if ret:
            if current_frame % step == 0:
                current_frame += 1
                yield ndarray_to_bytes(frame)
            current_frame += 1
        else:
            cam.release()
            cv2.destroyAllWindows()
            break


def image2bytes(file_info: FileInfo):
    save_uploaded_file(file_info)
    img_array = cv2.imread(os.path.join(DIR_OUT_PATH, file_info.name))
    return ndarray_to_bytes(img_array)


def save_uploaded_file(file_info: FileInfo, dir_out=DIR_OUT_PATH):
    try:
        if not os.path.exists(dir_out):
            os.makedirs(dir_out)
    except OSError:
        print("Error: Creating directory of data")

    file_path = os.path.join(dir_out, file_info.name)
    with open(file_path, "wb") as f:
        f.write(file_info.chunk)
    return file_path
