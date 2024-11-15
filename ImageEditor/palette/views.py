from django.shortcuts import render
from core.forms import ImageForm
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib import messages
from palette.functions import get_palette
import logging

logger = logging.getLogger(__name__)

class PaletteView(View):
    def get(self, request):
        form = ImageForm()
        context = {
            "form": form,
        }
        return render(request, "palette/upload.html", context)

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()
            url = obj.img.url
            palette = get_palette(url)
            context = {
                "url": url,
                "palette": palette,
            }
            return render(request, "palette/palette.html", context)
        else:
            messages.warning(request, 'Please select a Picture')
            logger.error("Please select a Picture")
            return HttpResponseRedirect(request.path)
