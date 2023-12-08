from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .models import CertificateApplication
# Create your views here.


class MarketPlaceView(TemplateView):
    template_name = 'market_place/index.html'


class CertificateApplicationView(ListView):
    model = CertificateApplication
    template_name = 'market_place/certificate/all.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CertificateApplicationView, self).get_context_data(object_list=None, **kwargs)
        context['certificate_applications'] = self.get_queryset()
        return context

    def get_queryset(self):
        return CertificateApplication.objects.all()
