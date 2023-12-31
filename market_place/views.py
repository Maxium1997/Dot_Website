from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.db.models import Q

from .models import CertificateApplication, Item
from .definitions import ItemStatus
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


class ItemIndexView(ListView):
    model = Item
    template_name = 'market_place/item/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemIndexView, self).get_context_data(object_list=None, **kwargs)
        items = list(set([_.name for _ in self.get_queryset()]))
        all_items = []

        for item in items:
            item_status_list = [item]
            for status in ItemStatus.__members__.values():
                criteria = Q(name__icontains=item) & Q(status__icontains=status.value[0])
                item_status_list.append(Item.objects.filter(criteria).count())
            all_items.append(item_status_list)

        context['item_status'] = ItemStatus.__members__.values()
        context['all_items'] = all_items

        return context

    def get_queryset(self):
        return Item.objects.all()
