from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from .forms import QRCodeForm, QRCodeReadForm
from .utils import generate_qr_code, read_qr_code
from django.conf import settings
import os
import cloudinary.uploader
from urllib.parse import unquote, urlparse
from django.http import JsonResponse
import cloudinary.uploader
# QR Code generation view
def generate_qr_view(request):
    if request.method == 'POST':
        form = QRCodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data']
            fill_color = form.cleaned_data.get('fill_color', 'black')
            back_color = form.cleaned_data.get('back_color', 'white')
            
            # Generate QR code and get the Cloudinary URL
            cloudinary_url = generate_qr_code(data, fill_color, back_color)
            
            return render(request, 'qr_module/generate_qr.html', {'filename': cloudinary_url})
    else:
        form = QRCodeForm()
    return render(request, 'qr_module/generate_qr.html', {'form': form})


# QR Code reading view
def read_qr_view(request):
    if request.method == 'POST':
        form = QRCodeReadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            # Upload to Cloudinary
            upload_response = cloudinary.uploader.upload(image_file, folder="uploaded_qr_codes")
            image_url = upload_response['url']
            data = read_qr_code(upload_response['url'])
            
            return render(request, 'qr_module/read_qr.html', {'form': form, 'data': data, 'image_url': image_url})
    else:
        form = QRCodeReadForm()
    
    return render(request, 'qr_module/read_qr.html', {'form': form})

def download_qr_code(request):
    # Extract 'filename' from the query string
    file_url = unquote(request.GET.get('filename', ''))

    if not file_url:
        return HttpResponse("File URL is missing", status=400)

    # Fetch the file from the URL
    response = requests.get(file_url, stream=True)

    if response.status_code == 200:
        # Extract file name
        file_name = file_url.split("/")[-1]
        content_type = response.headers['Content-Type']

        # Serve the file as a download
        response_stream = HttpResponse(response.content, content_type=content_type)
        response_stream['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response_stream
    else:
        return HttpResponse("File not found", status=404)
from django.http import JsonResponse
import cloudinary.uploader

def upload_qr_image(request):
    if request.method == 'POST' and request.FILES.get('image'):  # Ensure the 'image' file is in the request
        image_file = request.FILES['image']  # Get the uploaded file

        try:
            # Upload the image to Cloudinary
            upload_response = cloudinary.uploader.upload(image_file, folder="uploaded_qr_codes")
            image_url = upload_response['url']  # Get the uploaded image URL
            return JsonResponse({'success': True, 'image_url': image_url})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
