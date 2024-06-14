from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, ValidationError, PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.db.models import Q
from django.db import IntegrityError
from django.apps import apps
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView
from openpyxl import Workbook
import pandas as pd
# from openpyxl.writer.excel import save_virtual_workbook


from .models import OceanStation
from .definitions import OceanStationServiceItems
from organization.models import *

# Create your views here.


class BusinessView(TemplateView):
    template_name = 'business/index.html'

    def get_context_data(self, **kwargs):
        context = super(BusinessView, self).get_context_data(**kwargs)
        context['ocean_station_nums'] = OceanStation.objects.all().count()
        return context


class OceanStationIndexView(ListView):
    model = OceanStation
    template_name = 'business/OceanStation/index.html'


def import_ocean_station(request):
    ocean_station_exists = []
    ocean_station_creates = []

    if request.method == 'POST':
        try:
            excel_file = request.FILES['excel_file']

            # 讀取 Excel 文件
            df = pd.read_excel(excel_file)

            excel_data = []
            for index, row in df.iterrows():
                row_data = row.to_dict()
                excel_data.append(row_data)

            for data in excel_data:
                try:
                    ocean_station = OceanStation.objects.get(name=data.get('name'), address=data.get('address'))
                    ocean_station_exists.append(ocean_station)
                except IntegrityError:
                    break
                except ObjectDoesNotExist:
                    service_item = 0
                    for item in OceanStationServiceItems.__members__.values():
                        if item.value[2] in data.get('service_items'):
                            service_item += item.value[0]

                    ocean_station = OceanStation(
                        name=data.get('name'),
                        administrative_district=data.get('administrative_district'),
                        address=data.get('address'),
                        contact_number=data.get('contact_number'),
                        coordinate_longitude=data.get('coordinate_longitude'),
                        coordinate_latitude=data.get('coordinate_latitude'),
                        service_items=service_item,
                    )
                    ocean_station.save()
                    ocean_station_creates.append(ocean_station)
        except MultiValueDictKeyError:
            messages.warning(request, "Please upload a excel file.")
            return render(request, 'business/OceanStation/import.html')
        except:
            messages.warning(request, "Your file type is not accepted.")
            return render(request, 'business/OceanStation/import.html')

    return render(request, 'business/OceanStation/import.html', {'exist_ocean_stations': ocean_station_exists,
                                                                 'created_ocean_stations': ocean_station_creates})


class OceanStationUpdateView(UpdateView):
    model = OceanStation
    template_name = 'business/OceanStation/update.html'
    fields = ['administrative_district', 'address', 'contact_number', 'coordinate_longitude',
              'coordinate_latitude', 'fans_page_url']

    def get_object(self, queryset=None):
        return get_object_or_404(OceanStation, name=self.kwargs.get('ocean_station_name'))

    def get_context_data(self, **kwargs):
        context = super(OceanStationUpdateView, self).get_context_data(**kwargs)
        context['station'] = self.get_object()
        return context

    def get_success_url(self):
        messages.success(self.request, "Update successfully.")
        return reverse_lazy('ocean_station_update', kwargs={'ocean_station_name': self.get_object().name})


class OceanStationCoverPhotoUploadView(UpdateView):
    model = OceanStation
    template_name = 'business/OceanStation/cover_photo_upload.html'
    fields = ['cover_photo']

    def get_object(self, queryset=None):
        return get_object_or_404(OceanStation, name=self.kwargs.get('ocean_station_name'))

    def get_context_data(self, **kwargs):
        context = super(OceanStationCoverPhotoUploadView, self).get_context_data(**kwargs)
        context['station'] = self.get_object()
        return context

    def get_success_url(self):
        messages.success(self.request, "Update successfully.")
        return reverse_lazy('ocean_station_update', kwargs={'ocean_station_name': self.get_object().name})
