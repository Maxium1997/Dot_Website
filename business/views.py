from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class BusinessView(TemplateView):
    template_name = 'business/index.html'
