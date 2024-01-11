from abstractions.http_handler import HttpHandler


class ImageHandler:
    def __init__(self, http_handler: HttpHandler):
        self.http_handler = http_handler
        pass

    def send(self, chunk: bytes):
        return self.http_handler.send(chunk)
