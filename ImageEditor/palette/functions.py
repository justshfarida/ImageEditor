import cv2
import numpy as np
import urllib
from io import BytesIO
from colorthief import ColorThief

def get_palette(url):
    try:
        # Download the image
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        
        # Decode the image
        path = cv2.imdecode(arr, -1)
        if path is None:
            raise ValueError("Invalid image URL or unsupported image format")
        
        # Encode the image into a byte stream
        _, buffer = cv2.imencode('.png', path)
        byte_stream = BytesIO(buffer.tobytes())
        
        # Extract the palette using ColorThief
        color_thief = ColorThief(byte_stream)
        palette = color_thief.get_palette(color_count=6)
        return palette

    except urllib.error.URLError:
        raise ValueError("Invalid URL or network error while downloading the image")
    except cv2.error:
        raise ValueError("Error decoding the image, possibly unsupported format")
    except Exception as e:
        raise ValueError(f"Unexpected error occurred: {e}")
