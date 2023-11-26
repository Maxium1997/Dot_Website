from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class MarketPlaceView(TemplateView):
    template_name = 'market_place/index.html'
