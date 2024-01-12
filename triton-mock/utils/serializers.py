import numpy as np

from utils.bmsgpack import msgpack_to_obj, obj_to_msgpack


def ndarray_to_bytes(array: np.ndarray) -> bytes:
    return obj_to_msgpack(array)


def bytes_to_ndarray(byte_array: bytes) -> np.ndarray:
    obj = msgpack_to_obj(byte_array)
    if type(obj) == np.ndarray:
        obj = obj.copy()
    return obj
