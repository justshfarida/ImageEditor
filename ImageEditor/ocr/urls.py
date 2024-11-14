from django.urls import path, include
from . import views
from django.views.generic import RedirectView

app_name = "ocr"

urlpatterns = [
    path('', RedirectView.as_view(url='core/', permanent=True)),
    path('core/', include("core.urls")),   
    path('upload/', views.Upload.as_view(), name="upload"),
    path('preview/', views.Preview.as_view(), name="preview"),
]