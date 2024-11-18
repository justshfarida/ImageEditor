from django.shortcuts import render, redirect
from .forms import EncodeForm, DecodeForm
from .models import SteganographyImage
from .utils import encode_image, decode_image

def encode_view(request):
    if request.method == 'POST':
        form = EncodeForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            original_image = form.cleaned_data['original_image']
            message = form.cleaned_data['message']

            encoded_img = encode_image(original_image, message)
            encoded_img_path = f'steganography/encoded/{original_image.name}'
            encoded_img.save(encoded_img_path)

            instance.encoded_image = encoded_img_path
            instance.save()
            return render(request, 'steganography/encode_success.html', {'image': instance})
    else:
        form = EncodeForm()
    return render(request, 'steganography/encode.html', {'form': form})

def decode_view(request):
    if request.method == 'POST':
        form = DecodeForm(request.POST, request.FILES)
        if form.is_valid():
            encoded_image = request.FILES['encoded_image']
            decoded_message = decode_image(encoded_image)
            return render(request, 'steganography/decode_success.html', {'message': decoded_message})
    else:
        form = DecodeForm()
    return render(request, 'steganography/decode.html', {'form': form})
