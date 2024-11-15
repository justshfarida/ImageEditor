# palette/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("generate_palette/", views.PaletteView.as_view(), name="generate_palette"),
]
