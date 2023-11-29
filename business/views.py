from django.shortcuts import render
from django.views.generic import TemplateView, ListView


from .models import MobileStorageEquipment
from .definitions import CPC4Unit

# Create your views here.


class BusinessView(TemplateView):
    template_name = 'business/index.html'


class MobileStorageEquipmentView(ListView):
    model = MobileStorageEquipment
    template_name = 'business/MobileStorageEquipment/all.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MobileStorageEquipmentView, self).get_context_data(object_list=None, **kwargs)
        context['mobile_storage_equipments'] = MobileStorageEquipment.objects.all().order_by('manage_unit')
        return context
