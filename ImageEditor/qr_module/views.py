from pyexpat.errors import messages
from venv import logger
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import QRCodeForm
from core.models import Image  # Import the Image model
from core.forms import ImageForm  # Import the ImageForm
from .utils import generate_qr_code, read_qr_code
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
        form = ImageForm()
        return render(request, 'qr_module/read_qr.html', {"form": form})

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()  # Save the image instance
            qr_code_data = read_qr_code(obj.img.url)  # Read QR code from the uploaded image

            if not qr_code_data:
                qr_code_data = "No QR code detected."

            context = {
                "url": obj.img.url,
                "data": qr_code_data,
            }
            return render(request, 'qr_module/display_data.html', context)
        else:
            messages.error(request, "Please upload a valid image file.")
            return redirect(request.path)
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
