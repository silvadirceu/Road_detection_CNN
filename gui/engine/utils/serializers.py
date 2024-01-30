import os
import base64
import json
import numpy as np
from engine.utils.bmsgpack import msgpack_to_obj, obj_to_msgpack

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
