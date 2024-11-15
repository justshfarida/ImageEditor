# palette/urls.py
from django.urls import path
from . import views

app_name = "palette"

urlpatterns = [
    path("generate_palette/", views.PaletteView.as_view(), name="generate_palette"),
]
