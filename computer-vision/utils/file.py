from io import BytesIO
import cv2
import os
import pickle
from PIL import Image
import numpy as np

DIR_OUT_PATH = "."


class FileInfo:
    def __init__(self, name: str, chunk: bytes, path=""):
        self.name = name
        self.file_type = os.path.basename(self.name).split(".")[-1]
        self.chunk = chunk
        self.path = path


def video2image(file_info: FileInfo, step: int):
    save_uploaded_file(file_info)
    cam = cv2.VideoCapture(os.path.join(DIR_OUT_PATH, file_info.name))
    fps = round(cam.get(cv2.CAP_PROP_FPS))
    current_frame = 0
    while True:
        ret, frame = cam.read()
        if ret:
            if current_frame % step == 0:
                yield frame, fps * current_frame
            current_frame += 1
        else:
            cam.release()
            cv2.destroyAllWindows()
            break
    delete_file(file_info)

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


def delete_file(file_info: FileInfo, dir=DIR_OUT_PATH):
    path = os.path.join(dir, file_info.name)
    if os.path.exists(path):
        os.remove(path)
