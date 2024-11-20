import os
import cloudinary.uploader
import qrcode
from PIL import Image
import cv2
import numpy as np
import requests

# QR Code generator function
def generate_qr_code(data, fill_color='black', back_color='white'):
    try:
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
        response = cloudinary.uploader.upload(img, folder="generated_qr_codes")
        return response.get('url', None)
    except ValueError as e:
        raise ValueError(f"Error generating QR code: {e}")

# QR Code reader function
def read_qr_code(image_url):
    try:
        # Fetch the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        img_array = np.asarray(bytearray(response.content), dtype="uint8")
        
        # Decode the image into OpenCV format
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Use OpenCV's QRCodeDetector
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)

        # Check if data was found
        if not data:
            print("No QR code detected in the image.")
            return None

        return data
    except requests.exceptions.RequestException as e:
        print(f"HTTP request error: {e}")
        return None
    except cv2.error as e:
        print(f"OpenCV error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

