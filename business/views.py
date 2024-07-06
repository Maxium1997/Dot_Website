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
from django.views.generic import TemplateView, ListView, UpdateView, DetailView
from openpyxl import Workbook
import pandas as pd
import logging
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ocean_stations'] = OceanStation.objects.all()
        return context


def import_ocean_station(request):
    ocean_station_exists = []
    ocean_station_creates = []

    if not request.user.is_superuser:
        raise PermissionDenied

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
                    ocean_station = OceanStation.objects.get(oid=data.get('oid'),
                                                             name=data.get('name'),
                                                             address=data.get('address'))
                    ocean_station_exists.append(ocean_station)
                except IntegrityError:
                    break
                except ObjectDoesNotExist:
                    service_item = 0
                    for item in OceanStationServiceItems.__members__.values():
                        if item.value[2] in data.get('service_items'):
                            service_item += item.value[0]

                    ocean_station = OceanStation(
                        oid=data.get('oid'),
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
        # except:
        #     messages.warning(request, "Your file type is not accepted.")
        #     return render(request, 'business/OceanStation/import.html')

    return render(request, 'business/OceanStation/import.html', {'exist_ocean_stations': ocean_station_exists,
                                                                 'created_ocean_stations': ocean_station_creates})


class OceanStationUpdateView(UpdateView):
    model = OceanStation
    template_name = 'business/OceanStation/update.html'
    fields = ['administrative_district', 'address', 'contact_number', 'coordinate_longitude',
              'coordinate_latitude', 'fans_page_url']

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            # If the user is not a superuser, raise a permission denied error
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(OceanStation, name=self.kwargs.get('ocean_station_name'))

    def get_context_data(self, **kwargs):
        context = super(OceanStationUpdateView, self).get_context_data(**kwargs)
        context['station'] = self.get_object()
        return context

    def get_success_url(self):
        messages.success(self.request, "Update successfully.")
        return reverse_lazy('ocean_station_update', kwargs={'ocean_station_name': self.get_object().name})


class OceanStationDetailView(DetailView):
    model = OceanStation
    template_name = 'business/OceanStation/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(OceanStation, name=self.kwargs.get('ocean_station_name'))

    def get_context_data(self, **kwargs):
        context = super(OceanStationDetailView, self).get_context_data(**kwargs)
        station = self.get_object()
        context['station'] = station
        service_items = []
        for si in OceanStationServiceItems:
            if station.service_items & si.value[0]:
                service_items.append(True)
            else:
                service_items.append(False)
        context['service_items'] = service_items
        return context


logger = logging.getLogger(__name__)


class OceanStationCoverPhotoUploadView(UpdateView):
    model = OceanStation
    template_name = 'business/OceanStation/cover_photo_upload.html'
    fields = ['cover_photo']

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            # If the user is not a superuser, raise a permission denied error
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(OceanStation, name=self.kwargs.get('ocean_station_name'))

    def get_context_data(self, **kwargs):
        context = super(OceanStationCoverPhotoUploadView, self).get_context_data(**kwargs)
        context['station'] = self.get_object()
        return context

    def form_valid(self, form):
        ocean_station = self.get_object()
        # Check if a new cover photo is being uploaded
        if 'cover_photo' in form.changed_data:
            logger.info(f"New cover photo is being uploaded for OceanStation {ocean_station.pk}")
            # Delete the old cover photo
            ocean_station.delete_old_cover_photo()

        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Update successfully.")
        return reverse_lazy('ocean_station_update', kwargs={'ocean_station_name': self.get_object().name})
