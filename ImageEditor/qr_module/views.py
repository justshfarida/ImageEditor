from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import QRCodeForm
from core.models import Image  # Import the Image model
from core.forms import ImageForm  # Import the ImageForm
from .utils import generate_qr_code, read_qr_code
import cloudinary.uploader
from urllib.parse import unquote
import requests


class GenerateQRCodeView(View):
    def get(self, request):
        form = QRCodeForm()
        return render(request, 'qr_module/generate_qr.html', {'form': form})

    def post(self, request):
        form = QRCodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data']
            fill_color = form.cleaned_data.get('fill_color', 'black')
            back_color = form.cleaned_data.get('back_color', 'white')

            # Generate QR code and get Cloudinary URL
            cloudinary_url = generate_qr_code(data, fill_color, back_color)

            return render(request, 'qr_module/generate_qr.html', {'filename': cloudinary_url})
        return render(request, 'qr_module/generate_qr.html', {'form': form, 'error': 'Invalid input.'})


class ReadQRCodeView(View):
    def get(self, request):
        return render(request, 'qr_module/read_qr.html')

    def post(self, request):
        image_form = ImageForm(request.POST, request.FILES)

        if image_form.is_valid():
            # Save the image using ImageForm
            image_instance = image_form.save()
            image_url = image_instance.img.url  # Cloudinary URL

            try:
                # Read QR code data
                data = read_qr_code(image_url)
                if not data:
                    data = "No QR code detected."

                return render(request, 'qr_module/read_qr.html', {
                    'data': data,
                    'image_url': image_url,  # Pass the image URL for display
                })
            except Exception as e:
                return render(request, 'qr_module/read_qr.html', {
                    'error': f"Error processing QR code: {e}"
                })

        return render(request, 'qr_module/read_qr.html', {
            'error': 'Invalid input.'
        })


class DownloadQRCodeView(View):
    def get(self, request):
        file_url = unquote(request.GET.get('filename', ''))
        if not file_url:
            return HttpResponse("File URL is missing", status=400)

        try:
            response = requests.get(file_url, stream=True)
            if response.status_code == 200:
                file_name = file_url.split("/")[-1]
                content_type = response.headers['Content-Type']

                response_stream = HttpResponse(response.content, content_type=content_type)
                response_stream['Content-Disposition'] = f'attachment; filename="{file_name}"'
                return response_stream
            return HttpResponse("File not found", status=404)
        except Exception as e:
            return HttpResponse(f"Error during download: {e}", status=500)
