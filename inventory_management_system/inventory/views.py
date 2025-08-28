from django.shortcuts import render
from django.views.generic import TemplateView

# Basic homepage with - navbar, buttons for login and signup etc.

class Index(TemplateView):
    template_name = 'inventory/index.html'
