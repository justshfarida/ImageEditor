from django.shortcuts import render, redirect
from django.views import View
from ocr.functions import ocr
from core.models import Image
from core.forms import ImageForm 
from django.contrib import messages
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)

class Upload(View):
    def get(self, request):
        form = ImageForm()
        context = {
            "form": form,
            "languages": settings.OCR_LANGUAGES.items(),
            "default_lang": settings.DEFAULT_OCR_LANG,
        }
        return render(request, "ocr/upload.html", context)

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()
            request.session['id'] = obj.id
            language = request.POST.get("language")
            text = ocr(obj.img.url, language)
            logger.error(f"Text: {text}")
            context = {
                "url": obj.img.url,
                "text": text,
            }
            return render(request, "ocr/result.html", context)
        else:
            messages.warning(request, 'Please select a Picture')
            return HttpResponseRedirect(request.path)