import cv2
import numpy as np
import urllib
from io import BytesIO
from colorthief import ColorThief

def get_palette(url):
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        path = cv2.imdecode(arr, -1)
        _, buffer = cv2.imencode('.png', path)
        byte_stream = BytesIO(buffer.tobytes())
        color_thief = ColorThief(byte_stream)
        palette = color_thief.get_palette(color_count=6)
        return palette