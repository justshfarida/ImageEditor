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
        try:
            form = ImageForm(request.POST, request.FILES)

            if form.is_valid():
                obj = form.save()
                request.session['id'] = obj.id
                language = request.POST.get("language", "en")
                try:
                    text = ocr(obj.img.url, language)
                except Exception as e:
                    logger.error(f"OCR processing failed for image {obj.img.url}. Error: {e}", exc_info=True)
                    messages.error(request, "An error occurred while processing the image. Please try again.")
                    return HttpResponseRedirect(request.path)

                context = {
                    "url": obj.img.url,
                    "text": text,
                }
                return render(request, "ocr/result.html", context)
            else:
                logger.warning(f"Form validation failed. Errors: {form.errors}")
                messages.warning(request, 'Please select a valid picture.')
                return HttpResponseRedirect(request.path)

        except Exception as e:
            logger.critical(f"Unexpected error in post method: {e}", exc_info=True)
            messages.error(request, "An unexpected error occurred. Please try again later.")
            return HttpResponseRedirect(request.path)