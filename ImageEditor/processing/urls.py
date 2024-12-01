from django.urls import path, include
from . import views
from django.views.generic import RedirectView
from processing.views import Upload, ProcessImage, SelectChoice

app_name = 'processing'

urlpatterns = [
  path('', RedirectView.as_view(url='core/', permanent=True)),
  path('core/', include('core.urls')),
  path("upload/", Upload.as_view(), name='upload'),
  path("select_choice/", SelectChoice.as_view(), name="select_choice"),
  path("process/<int:choice>/", ProcessImage.as_view(), name="process"),
]