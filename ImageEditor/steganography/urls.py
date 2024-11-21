from django.urls import path
from . import views

app_name = "steganography"

urlpatterns = [
    path("upload/<str:action>/", views.upload_view, name="upload"),
]
