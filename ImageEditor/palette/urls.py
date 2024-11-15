# palette/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("generate_palette/", views.generate_palette, name="generate_palette"),
]
