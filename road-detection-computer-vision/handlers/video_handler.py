from abstractions.http_handler import HttpHandler
from utils.file import FileInfo, video2image

class VideoHandler:
    def __init__(self, http_handler: HttpHandler):
        self.http_handler = http_handler
        pass
        

    def send(self, chunk: bytes):
        file_info = FileInfo("dump.mp4", chunk)
        frames_generator = video2image(file_info, 20)
        for frames_chunk in frames_generator:
            yield self.http_handler.send(frames_chunk)

