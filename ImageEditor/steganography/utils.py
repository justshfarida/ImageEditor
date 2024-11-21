from PIL import Image
import io
import os
from django.conf import settings

def encode_message(image, message):
    """Encode a message into an image."""
    img = Image.open(image)
    encoded = img.copy()
    width, height = img.size
    message += "§"  # Append a delimiter to indicate the end of the message
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    data_index = 0

    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for n in range(3):  # Modify R, G, B values
                if data_index < len(binary_message):
                    pixel[n] = pixel[n] & ~1 | int(binary_message[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    output = io.BytesIO()
    encoded.save(output, format="PNG")
    output.seek(0)
    return output

def decode_message(image):
    """Decode a hidden message from an image."""
    img = Image.open(image)
    binary_message = ""
    for pixel in img.getdata():
        for value in pixel[:3]:  # Read R, G, B values
            binary_message += str(value & 1)

    # Convert binary to text
    decoded_message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        char = chr(int(byte, 2))
        if char == "§":  # Stop at delimiter
            break
        decoded_message += char

    return decoded_message


def save_image(encoded_image):
    """Save the encoded image from BytesIO to the media directory."""
    file_name = "encoded_image.png"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    
    # Write BytesIO to file
    with open(file_path, "wb") as f:
        f.write(encoded_image.getvalue())
    
    return os.path.join(settings.MEDIA_URL, file_name)
