import os
import base64
import json

class FileInfo:
    def __init__(self, name: str, chunk: bytes, path=""):
        self.name = name
        self.format = os.path.basename(self.name).split(".")[-1]
        self.chunk = chunk
        self.path = path

    def to_dict(self):
        return {
            'name': self.name,
            'format': self.format,
            'chunk': base64.b64encode(self.chunk).decode('utf-8'),  # Assuming chunk is bytes and needs to be converted to a string
            'path': self.path
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            chunk=base64.b64decode(data['chunk']),  # Assuming chunk is stored as a string and needs to be converted back to bytes
            path=data['path']
        )
