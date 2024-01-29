import os
import base64
import json
import numpy as np
from engine.utils.bmsgpack import msgpack_to_obj, obj_to_msgpack

#REVIEW: importing again due to circular import
class FileInfo:
    def __init__(self, name: str, chunk: bytes, path=""):
        self.name = name
        self.format = os.path.basename(self.name).split(".")[-1]
        self.chunk = chunk
        self.path = path

def ndarray_to_bytes(array: np.ndarray) -> bytes:
    return obj_to_msgpack(array)


def bytes_to_ndarray(byte_array: bytes) -> np.ndarray:
    obj = msgpack_to_obj(byte_array)
    if type(obj) == np.ndarray:
        obj = obj.copy()
    return obj


def bytes_to_base64_utf8encoded(bytes):
    base64Bytes = base64.b64encode(bytes)
    unicodeContent = json.dumps(base64Bytes.decode("utf-8"))
    return unicodeContent


def read_all_bytes(filename):
    in_file = open(filename, "rb")
    bytes = in_file.read()
    in_file.close()
    return bytes



def json_celery_serializer(file_info):
    file_bytes = file_info.getvalue()
    chunk_base64 = base64.b64encode(file_bytes).decode('utf-8')
    file_info_dict = {
        "name": file_info.name,
        "chunk": chunk_base64, 
        "path": "",
    }
    file_info_json = json.dumps(file_info_dict)
    return file_info_json


# TODO: will be removed
def post_celery_serialize(file_info):
    file_info_dict = json.loads(file_info)

    # Decode base64-encoded chunk back to bytes
    chunk_bytes = base64.b64decode(file_info_dict["chunk"])

    # Create the original file_info object
    original_file_info = FileInfo(
        name=file_info_dict["name"], chunk=chunk_bytes, path=file_info_dict["path"]
    )
    return original_file_info
