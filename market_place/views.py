from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.db.models import Q

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


class CertificateApplicationSearchView(ListView):
    template_name = 'market_place/certificate/search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CertificateApplicationSearchView, self).get_context_data(object_list=None, **kwargs)
        context['certificate_applications'] = self.get_queryset()
        return context

    def get_queryset(self):
        keywords = self.request.GET.get('keywords')
        keywords = keywords.split()
        q_objects = Q()
        for keyword in keywords:
            q_objects |= Q(applicant_name__icontains=keyword)
            q_objects |= Q(applicant_contact_number__icontains=keyword)
            q_objects |= Q(custodian_name__icontains=keyword)
            q_objects |= Q(custodian_ID_number__icontains=keyword)
            q_objects |= Q(custodian_contact_number__icontains=keyword)
        # search_criteria = Q(applicant_name=keyword) | Q(custodian_name=keyword) | Q(custodian_ID_number=keyword)
        return CertificateApplication.objects.filter(q_objects)
