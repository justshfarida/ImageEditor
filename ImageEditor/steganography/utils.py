from PIL import Image

def encode_image(image_path, message):
    img = Image.open(image_path)
    binary_message = ''.join(format(ord(i), '08b') for i in message)
    binary_message += '1111111111111110'  # End-of-message delimiter

    if img.mode != 'RGB':
        img = img.convert('RGB')

    encoded_img = img.copy()
    width, height = img.size
    pixels = list(img.getdata())
    binary_index = 0

    for i in range(len(pixels)):
        r, g, b = pixels[i]
        if binary_index < len(binary_message):
            r = (r & ~1) | int(binary_message[binary_index])
            binary_index += 1
        if binary_index < len(binary_message):
            g = (g & ~1) | int(binary_message[binary_index])
            binary_index += 1
        if binary_index < len(binary_message):
            b = (b & ~1) | int(binary_message[binary_index])
            binary_index += 1
        pixels[i] = (r, g, b)

    encoded_img.putdata(pixels)
    return encoded_img

def decode_image(image_path):
    img = Image.open(image_path)
    binary_message = ''
    pixels = list(img.getdata())

    for r, g, b in pixels:
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)

    binary_chars = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]
    decoded_message = ''.join(chr(int(b, 2)) for b in binary_chars if b != '11111111')
    return decoded_message.split('1111111111111110')[0]
