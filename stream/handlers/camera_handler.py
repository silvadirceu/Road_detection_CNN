from threading import Thread
from time import sleep
import cv2
from abstractions.http_client import HttpClient
from utils.serializers import ndarray_to_bytes
import logging


class CameraHandler:
    def __init__(self, httpHandler: HttpClient, connection_string: str):
        if not connection_string:
            raise TypeError("Camera connection string cannot be a Falsy value")
        self.http_handler = httpHandler
        self.connection_string = connection_string
        pass

    def __send_video(self, fps, step, tries=5):
        logging.log(1, "Connecting to camera host")
        cap = cv2.VideoCapture(self.connection_string)
        curr_try = 0
        while not cap.isOpened() and curr_try < tries:
            cap.open(self.connection_string)
            logging.warning(f"{curr_try}: Connection failed")
            curr_try+=1
            sleep(15)
        logging.log(1, "Connection sucessfull with the host")
        
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame_count += 1
                if frame_count % (step * fps) == 0:
                    self.http_handler.send(ndarray_to_bytes(frame))
            else:
                logging.warning(f"Error getting frame.")
                break

    def send_video_parallel(self, fps=30, step=2):
        thread = Thread(target=self.__send_video(fps, step))
        thread.start()
        return thread
