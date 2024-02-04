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
    
    @staticmethod
    def to_frame(chunk: bytes, step=20):
        frames = iio.imread(chunk, index=None, format_hint=".mp4")
        fps = 30 #iio.immeta(chunk)["fps"]
        current_frame = 0
        for frame in iio.imiter(chunk, format_hint=".mp4"):
            if current_frame % step == 0:
                yield frame, current_frame
            current_frame+=1
