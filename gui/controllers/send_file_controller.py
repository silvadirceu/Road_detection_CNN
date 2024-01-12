from abstractions.controller import Controller
from abstractions.http_handler import HttpHandler
from engine.utils.file import image2bytes, video2image
from engine.utils.file import FileInfo
from proto.grpc_client import Grpc_Client


class SendFileController(Controller):
    def __init__(self, http_handler: Grpc_Client):
        self.http_handler = http_handler

    def __send_video(self, chunk: FileInfo):
        return self.http_handler.send_video(chunk)

    def __send_image(self, chunk: FileInfo):
        return self.http_handler.send_image(chunk)

    def send(self, file_info: FileInfo):
        filename = file_info.name
        file_extension = filename.split(".")[-1].lower()
        if file_extension in ["mp4", "avi"]:
            return self.__send_video(file_info.chunk)
        elif file_extension in ["png", "jpg"]:
            return self.__send_image(file_info.chunk)
