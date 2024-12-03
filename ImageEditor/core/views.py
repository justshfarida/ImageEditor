from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.core import mail
from django.conf import settings
from prometheus_client import generate_latest, REGISTRY
from prometheus_client.exposition import basic_auth_handler
from django.http import HttpResponse

def metrics(request):
    return HttpResponse(generate_latest(REGISTRY), content_type="text/plain; version=0.0.4; charset=utf-8")

# define the home view
class HomeView(TemplateView):
    '''
    Sets the home page.
    '''
    template_name = 'index.html'

class AboutView(TemplateView):
    '''
    Sets the about page.
    '''
    template_name = 'about.html'