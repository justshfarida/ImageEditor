import cv2
import numpy as np
from io import BytesIO
from stegano import lsb  # Only using lsb now

# Hide a message using LSB (Least Significant Bit) method
def hide_lsb(img, msg="Demo Message"):
    is_success, buffer = cv2.imencode(".png", img)
    io_buf = BytesIO(buffer)
    
    # Hide the message in the image using LSB
    hid = lsb.hide(io_buf, msg)
    
    # Save the image with hidden message
    io_res = BytesIO()
    hid.save(io_res, "PNG")
    decode_img = cv2.imdecode(np.frombuffer(io_res.getbuffer(), np.uint8), -1)
    
    is_success, buffer = cv2.imencode(".png", decode_img)
    io_buf = BytesIO(buffer)
    return io_buf

# Reveal the hidden message using LSB
def reveal_lsb(img):
    is_success, buffer = cv2.imencode(".png", img)
    io_buf = BytesIO(buffer)
    
    # Extract the hidden message from the image
    msg = lsb.reveal(io_buf)
    
    return msg, io_buf
