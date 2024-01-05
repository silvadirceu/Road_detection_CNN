from typing import Any
import cv2
import os
from engine.utils.data import read_all_bytes
from streamlit.runtime.uploaded_file_manager import UploadedFile

DIR_OUT_PATH = "data"


def video2image(file_name: str, step: int, dir_out: str = DIR_OUT_PATH):
    cam = cv2.VideoCapture(file_name)
    try:
        if not os.path.exists(dir_out):
            os.makedirs(dir_out)
    except OSError:
        print("Error: Creating directory of data")

    current_frame = 0
    while True:
        ret, frame = cam.read()

        if ret:
            if current_frame % step == 0:
                name = os.path.join(dir_out, "frame" + str(current_frame) + ".jpg")
                cv2.imwrite(name, frame)
                img_bytes = read_all_bytes(name)
                current_frame += 1
                yield img_bytes, current_frame

            current_frame += 1
        else:
            cam.release()
            cv2.destroyAllWindows()
            break


def save_uploaded_file(uploaded_file: UploadedFile, dir_out=DIR_OUT_PATH):
    try:
        if not os.path.exists(dir_out):
            os.makedirs(dir_out)
    except OSError:
        print("Error: Creating directory of data")

    file_path = os.path.join(dir_out, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path
