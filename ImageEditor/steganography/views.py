from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import EncodeForm, DecodeForm
from .utils import encode_message, decode_message
from django.core.files.storage import default_storage
from django.conf import settings
import os
from .utils import save_image


def upload_view(request, action):
    if action == "encode":
        is_encoding = True
        form_class = EncodeForm
    else:
        is_encoding = False
        form_class = DecodeForm

    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            if is_encoding:
                # Encoding logic
                message = form.cleaned_data["message"]
                encoded_image = encode_message(image, message)
                file_path = save_image(encoded_image)
                return render(request, "success.html", {"is_encoding": True, "image_url": file_path})
            else:
                # Decoding logic
                decoded_message = decode_message(image)
                return render(request, "success.html", {"is_encoding": False, "message": decoded_message})
    else:
        form = form_class()

    return render(request, "steganography/success.html", {"is_encoding": True, "image_url": file_path})