from django.urls import path
from . import views
from core.views import HomeView, AboutView
from django.urls import path, include

app_name = "core"

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('about', AboutView.as_view(), name='about'),
     path("palette/", include("palette.urls")),
]