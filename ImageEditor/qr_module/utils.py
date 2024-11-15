import os
import cloudinary.uploader
import qrcode
from PIL import Image
import cv2
import numpy as np
import requests

# QR Code generator function
def generate_qr_code(data, fill_color='black', back_color='white'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Save to Cloudinary
    img.save("temp_qr.png")
    response = cloudinary.uploader.upload("temp_qr.png", folder="generated_qr_codes")
    os.remove("temp_qr.png")
    
    return response['url']

# QR Code reader function
def read_qr_code(image_url):
    resp = requests.get(image_url, stream=True).raw
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    
    return data
