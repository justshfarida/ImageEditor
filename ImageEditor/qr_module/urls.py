from django.urls import path
from .views import GenerateQRCodeView, ReadQRCodeView, DownloadQRCodeView
app_name = 'qr_module'

urlpatterns = [
    path('generate/', GenerateQRCodeView.as_view(), name='generate_qr'),
    path('read/', ReadQRCodeView.as_view(), name='read_qr'),
    path('download/', DownloadQRCodeView.as_view(), name='download_qr'),
]
