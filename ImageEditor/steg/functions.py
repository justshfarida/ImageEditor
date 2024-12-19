import cv2
import numpy as np
from io import BytesIO
from stegano import lsb


def hide_lsb(img, msg="Demo Message"):
    is_success, buffer = cv2.imencode(".png", img)
    io_buf = BytesIO(buffer)
    hid = lsb.hide(io_buf, msg)
    io_res = BytesIO()
    hid.save(io_res, "PNG")
    decode_img = cv2.imdecode(np.frombuffer(io_res.getbuffer(), np.uint8), -1)
    is_success, buffer = cv2.imencode(".png", decode_img)
    io_buf = BytesIO(buffer)
    return io_buf


def reveal_lsb(img):
    is_success, buffer = cv2.imencode(".png", img)
    io_buf = BytesIO(buffer)
    msg = lsb.reveal(io_buf)
    io_buf = BytesIO(buffer)
    return msg, io_buf