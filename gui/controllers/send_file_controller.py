from abstractions.controller import Controller
from abstractions.http_handler import HttpHandler
from engine.utils.file import image2bytes, video2image
from engine.utils.file import FileInfo


class SendFileController(Controller):
    def __init__(self, http_handler: HttpHandler):
        self.http_handler = http_handler

    def send(self, file_info: FileInfo):
        return self.http_handler.send(file_info.chunk, file_info.format)
