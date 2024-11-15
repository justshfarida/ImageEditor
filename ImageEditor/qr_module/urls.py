from django.urls import path
from . import views
app_name = 'qr_module'  # Add app_name to namespace the URL patterns

urlpatterns = [
    path('generate/', views.generate_qr_view, name='generate_qr'),
    path('read/', views.read_qr_view, name='read_qr'),
    path('download/', views.download_qr_code, name='download_qr'),  # Add this line
    path('upload/', views.upload_qr_image, name='upload_qr')
]
