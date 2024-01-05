import base64
import json


def bytes_to_base64_utf8encoded(bytes):
    base64Bytes = base64.b64encode(bytes)
    unicodeContent = json.dumps(base64Bytes.decode("utf-8"))
    return unicodeContent


def read_all_bytes(filename):
    in_file = open(filename, "rb")
    bytes = in_file.read()
    in_file.close()
    return bytes
