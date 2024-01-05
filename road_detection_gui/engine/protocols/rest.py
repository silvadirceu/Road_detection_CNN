import requests
from engine.protocols.protocol import Protocol
from ..utils.data import bytes_to_base64_utf8encoded, read_all_bytes


class Rest(Protocol):
    def __init__(self, api_url):
        self.api_url = api_url

    def send(self, chunk: bytes):
        file_base64 = bytes_to_base64_utf8encoded(chunk)
        response = requests.post(
            self.api_url + "predict", data={"file_base64": file_base64}
        )
        return response
