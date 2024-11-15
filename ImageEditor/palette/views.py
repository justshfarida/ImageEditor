from django.shortcuts import render

# Create your views here.
# palette/views.py
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from colorthief import ColorThief
from PIL import Image
import os


def generate_palette(request):
    if request.method == "POST" and request.FILES["image"]:
        uploaded_image = request.FILES["image"]
        fs = FileSystemStorage()
        filename = fs.save(uploaded_image.name, uploaded_image)
        file_url = fs.url(filename)  # Get the file URL to pass to the template

        # Use ColorThief to get dominant colors
        image_path = fs.path(filename)
        color_thief = ColorThief(image_path)
        palette = color_thief.get_palette(color_count=6)  # Get top 6 colors

        return render(request, "palette/palette.html", {"palette": palette, "file_url": file_url})

    return render(request, "palette/upload.html")
