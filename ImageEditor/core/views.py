from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.core import mail
from django.conf import settings

# define the home view
class HomeView(TemplateView):
    '''
    Sets the home page.
    '''
    template_name = 'ImageEditor/templates/index.html'

class AboutView(TemplateView):
    '''
    Sets the about page.
    '''
    template_name = 'ImageEditor/templates/about.html'