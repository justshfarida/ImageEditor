# palette/urls.py
from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = "palette"

urlpatterns = [
    path('', RedirectView.as_view(url='core/', permanent=True)),
    path("generate_palette/", views.PaletteView.as_view(), name="generate_palette"),
]
