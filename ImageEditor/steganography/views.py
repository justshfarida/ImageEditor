from email.mime import image
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from .forms import SteganographyForm
from .models import SteganographyModel
from django.contrib import messages
from django.http import HttpResponseRedirect
import cv2
import numpy as np
import urllib.request
import requests

from steganography.functions import hide_lsb, reveal_lsb

CHOICES_WITH_CLASSES = {"LSB Hide":"prevent", "LSB Reveal":""}
CHOICES = ["LSB Hide", "LSB Reveal"]

class ProcessImage(View):
    def post(self, request, choice):
        id = request.session.get("id")
        obj = SteganographyModel.objects.get(id=id)

        # Retrieve the image
        url = obj.img.url
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        path = cv2.imdecode(arr, -1)  # Load image as it is

        content_type = "image/png"
        file_name = "processed_image.png"
        sec_msg = request.session.get("message", None)

        # Process based on the choice
        if choice == 0:  # LSB Hide
            img = hide_lsb(path, sec_msg)
        elif choice == 1:  # LSB Reveal
            msg, img = reveal_lsb(path)
            return render(request, "steganography/reveal.html", {"msg": msg})
        else:
            return HttpResponse("Invalid Option")

        option = request.POST.get("type")

        if option == "Preview":
            image_data = img.getvalue()
            return HttpResponse(image_data, content_type=content_type)
        elif option == "Download":
            return FileResponse(img, as_attachment=True, filename=file_name)
        else:
            return HttpResponse("Invalid Option")

class SelectChoice(View):
    def get(self, request):

        id = request.session.get("id")
        obj = SteganographyModel.objects.get(id=id)
        context={
                "object": obj, 
                "choices": CHOICES,
                "choices_with_classes": CHOICES_WITH_CLASSES
                }
        return render(request, "steganography/select_choice.html", context)

    def post(self, request):

        type = request.POST.get("type")
        request.session["message"] = request.POST.get("message", None)
        if type:    
            choice_id = CHOICES.index(type)
            
            return redirect((reverse_lazy("steganography:process", kwargs={"choice": choice_id})))
        else:
            return HttpResponse("Invalid Choice")

class Upload(View):
    def get(self, request):
        form = SteganographyForm()
        context = {
            "form": form,
        }
        return render(request, "steganography/upload.html", context)
    
    def post(self, request):
        form = SteganographyForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()
            request.session['id'] = obj.id     

            return redirect(reverse_lazy("steganography:select-choice"))
        else:
            messages.warning(request, 'Please select a Picture')
            return HttpResponseRedirect(request.path)