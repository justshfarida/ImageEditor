import easyocr

def ocr(image_path, lang):
    reader = easyocr.Reader([lang])
    result = reader.readtext(image_path)
    return result