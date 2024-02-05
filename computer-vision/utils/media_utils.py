from io import BytesIO
from PIL import Image
import numpy as np
import imageio.v3 as iio


class ImageUtils:
    @staticmethod
    def to_nddaray(chunk: bytes):
        img = Image.open(BytesIO(chunk))
        img = img.convert("RGB")
        return np.array(img)
        

class VideoUtils:
    @staticmethod
    def to_frames(chunk: bytes, step=20):
        fps = iio.immeta(chunk)["fps"]
        current_frame = 0
        for frame in iio.imiter(chunk, format_hint=".mp4"):
            if current_frame % step == 0:
                yield frame, current_frame*fps
            current_frame+=1
