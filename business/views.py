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


from .models import MobileStorageEquipment, MobileDevice, CertificateApplication, OceanStation
from .definitions import OceanStationServiceItems
from organization.models import *
from organization.definitions import CPC4Unit, ArmyCommission

# Create your views here.


class BusinessView(TemplateView):
    template_name = 'business/index.html'

    def get_context_data(self, **kwargs):
        context = super(BusinessView, self).get_context_data(**kwargs)
        context['mobile_storage_equipment_nums'] = MobileStorageEquipment.objects.all().count()
        context['mobile_device_nums'] = MobileDevice.objects.all().count()
        context['certificate_application_nums'] = CertificateApplication.objects.all().count()
        context['ocean_station_nums'] = OceanStation.objects.all().count()
        return context


class MobileStorageEquipmentView(ListView):
    model = MobileStorageEquipment
    template_name = 'business/MobileStorageEquipment/all.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MobileStorageEquipmentView, self).get_context_data(object_list=None, **kwargs)

        # Get the app configuration for the specified app
        app_config = apps.get_app_config('organization')
        # Get all models from the specified app
        app_models = app_config.get_models()
        # Name of the model to exclude
        model_to_exclude = 'BasicOrgInfo'
        # Filter models excluding the one specified
        filtered_models = [model for model in app_models if model.__name__ != model_to_exclude]

        manage_units = []
        manage_unit_options = []

        for mse in MobileStorageEquipment.objects.all():
            # Now, app_models is a list of model classes in the 'organization' app
            for model in filtered_models:
                try:
                    manage_units.append(model.objects.get(id=mse.manage_unit_object_id))
                    break
                except ObjectDoesNotExist:
                    pass

        for model in apps.get_app_config('organization').get_models():
            if model.__name__ == 'BasicOrgInfo':
                pass
            else:
                for item in model.objects.all():
                    if item.serial_number is None:
                        pass
                    else:
                        manage_unit_options.append((item.serial_number, item))

        context['mobile_storage_equipments'] = zip(self.get_queryset(), manage_units)
        context['count_mobile_storage_equipments'] = len(list(zip(self.get_queryset(), manage_units)))
        context['manage_unit_options'] = manage_unit_options

        return context

    def get_queryset(self):
        return MobileStorageEquipment.objects.all().order_by('manage_unit_content_type', 'manage_unit_object_id')


class MobileStorageEquipmentFilteredView(ListView):
    template_name = 'business/MobileStorageEquipment/filtered.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MobileStorageEquipmentFilteredView, self).get_context_data(object_list=None, **kwargs)

        if self.request.GET.get('manage_unit_option') == "":
            context['manage_unit_option'] = ""
        else:
            context['manage_unit_option'] = self.request.GET.get('manage_unit_option')

        # Get the app configuration for the specified app
        app_config = apps.get_app_config('organization')
        # Get all models from the specified app
        app_models = app_config.get_models()
        # Name of the model to exclude
        model_to_exclude = 'BasicOrgInfo'
        # Filter models excluding the one specified
        filtered_models = [model for model in app_models if model.__name__ != model_to_exclude]

        manage_units = []
        manage_unit_options = []

        for mse in self.get_queryset():
            # Now, app_models is a list of model classes in the 'organization' app
            for model in filtered_models:
                try:
                    if model.__name__ == 'BasicOrgInfo':
                        break
                    else:
                        manage_units.append(model.objects.get(id=mse.manage_unit_object_id))
                except ObjectDoesNotExist:
                    pass

        for model in apps.get_app_config('organization').get_models():
            if model.__name__ == 'BasicOrgInfo':
                pass
            else:
                for item in model.objects.all():
                    if item.serial_number is None:
                        pass
                    else:
                        if item.serial_number is None:
                            pass
                        else:
                            manage_unit_options.append((item.serial_number, item))

            context['mobile_storage_equipments'] = zip(self.get_queryset(), manage_units)
            context['count_mobile_storage_equipments'] = len(list(zip(self.get_queryset(), manage_units)))
            context['manage_unit_options'] = manage_unit_options
        return context

    def get_queryset(self):
        app_name = 'organization'
        # Get the app configuration for the specified app
        app_config = apps.get_app_config(app_name)
        # Get all models from the specified app
        app_models = app_config.get_models()
        # Name of the model to exclude
        model_to_exclude = 'BasicOrgInfo'
        # Filter models excluding the one specified
        filtered_models = [model for model in app_models if model.__name__ != model_to_exclude]
        query = []

        try:
            manage_unit_option = self.request.GET.get('manage_unit_option')
            if manage_unit_option == "":
                query.extend(MobileStorageEquipment.objects.all())
            else:
                # Now, app_models is a list of model classes in the 'organization' app
                for model in filtered_models:
                    try:
                        ta = model.objects.get(serial_number=manage_unit_option).id
                        # ta.objects.get()
                        query.extend(MobileStorageEquipment.objects.filter(manage_unit_object_id=ta))
                        break
                    except ObjectDoesNotExist:
                        pass

        except ValidationError:
            query.append(None)
        return query


class MobileDeviceView(ListView):
    model = MobileDevice
    template_name = 'business/MobileDevice/all.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MobileDeviceView, self).get_context_data(object_list=None, **kwargs)
        # Get the app configuration for the specified app
        app_config = apps.get_app_config('organization')
        # Get all models from the specified app
        app_models = app_config.get_models()
        # Name of the model to exclude
        model_to_exclude = 'BasicOrgInfo'
        # Filter models excluding the one specified
        filtered_models = [model for model in app_models if model.__name__ != model_to_exclude]

        owner_units = []
        owner_unit_options = []

        for md in self.get_queryset():
            # Now, app_models is a list of model classes in the 'organization' app
            for model in filtered_models:
                try:
                    owner_units.append(model.objects.get(id=md.owner_unit_object_id))
                    break
                except ObjectDoesNotExist:
                    pass

        for model in apps.get_app_config('organization').get_models():
            if model.__name__ == 'BasicOrgInfo':
                pass
            else:
                for item in model.objects.all():
                    if item.serial_number is None:
                        pass
                    else:
                        if item.serial_number is None:
                            pass
                        else:
                            owner_unit_options.append((item.serial_number, item))

        context['mobile_devices'] = zip(self.get_queryset(), owner_units)
        context['count_mobile_devices'] = len(list(zip(self.get_queryset(), owner_units)))
        context['owner_unit_options'] = owner_unit_options

        return context

    def get_queryset(self):
        return MobileDevice.objects.all().order_by('owner_unit_content_type', 'owner_unit_object_id', '-owner_commission')


class MobileDeviceFilteredView(ListView):
    template_name = 'business/MobileDevice/filtered.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MobileDeviceFilteredView, self).get_context_data(object_list=None, **kwargs)

        if self.request.GET.get('owner_unit_option') == "":
            context['owner_unit_option'] = ""
        else:
            context['owner_unit_option'] = self.request.GET.get('owner_unit_option')

        # Get the app configuration for the specified app
        app_config = apps.get_app_config('organization')
        # Get all models from the specified app
        app_models = app_config.get_models()
        # Name of the model to exclude
        model_to_exclude = 'BasicOrgInfo'
        # Filter models excluding the one specified
        filtered_models = [model for model in app_models if model.__name__ != model_to_exclude]
        owner_units = []
        owner_unit_options = []

        try:
            for md in self.get_queryset():
                # Now, app_models is a list of model classes in the 'organization' app
                for model in filtered_models:
                    try:
                        owner_units.append(model.objects.get(id=md.owner_unit_object_id))
                        break
                    except ObjectDoesNotExist:
                        pass

            for model in apps.get_app_config('organization').get_models():
                if model.__name__ == 'BasicOrgInfo':
                    pass
                else:
                    for item in model.objects.all():
                        if item.serial_number is None:
                            pass
                        else:
                            owner_unit_options.append((item.serial_number, item))

            context['mobile_devices'] = zip(self.get_queryset(), owner_units)
            context['count_mobile_devices'] = len(list(zip(self.get_queryset(), owner_units)))
        except TypeError:
            pass

        context['owner_unit_options'] = owner_unit_options
        return context

    def get_queryset(self):
        app_name = 'organization'
        # Get the app configuration for the specified app
        app_config = apps.get_app_config(app_name)
        # Get all models from the specified app
        app_models = app_config.get_models()
        # Name of the model to exclude
        model_to_exclude = 'BasicOrgInfo'
        # Filter models excluding the one specified
        filtered_models = [model for model in app_models if model.__name__ != model_to_exclude]
        query = []

        try:
            owner_unit_option = self.request.GET.get('owner_unit_option')
            if owner_unit_option == "" or owner_unit_option is None:
                return MobileDevice.objects.all().order_by('owner_unit_content_type', 'owner_unit_object_id', '-owner_commission')
            else:
                # Now, app_models is a list of model classes in the 'organization' app
                for model in filtered_models:
                    try:
                        ta = model.objects.get(serial_number=owner_unit_option).id
                        # ta.objects.get()
                        query.append(MobileDevice.objects.filter(owner_unit_object_id=ta))
                        break
                    except ObjectDoesNotExist:
                        pass

                result_query = query[0]
                for _ in query[0:]:
                    result_query = result_query.union(_)
                return result_query.order_by('-owner_commission')

        except ValidationError:
            return MobileDevice.objects.all().order_by('owner_unit_content_type', 'owner_unit_object_id', '-owner_commission')


class CertificateApplicationView(ListView):
    model = CertificateApplication
    template_name = 'business/Certificate/all.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CertificateApplicationView, self).get_context_data(object_list=None, **kwargs)
        # Get the app configuration for the specified app
        app_config = apps.get_app_config('organization')
        # Get all models from the specified app
        app_models = app_config.get_models()
        # Name of the model to exclude
        model_to_exclude = 'BasicOrgInfo'
        # Filter models excluding the one specified
        filtered_models = [model for model in app_models if model.__name__ != model_to_exclude]

        applicant_units = []
        owner_unit_options = []

        for md in self.get_queryset():
            # Now, app_models is a list of model classes in the 'organization' app
            for model in filtered_models:
                try:
                    applicant_units.append(model.objects.get(id=md.applicant_unit_object_id))
                    break
                except ObjectDoesNotExist:
                    pass

        context['certificate_applications'] = zip(self.get_queryset(), applicant_units)

        return context

    def get_queryset(self):
        return CertificateApplication.objects.all()


class CertificateApplicationSearchView(ListView):
    template_name = 'business/Certificate/search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CertificateApplicationSearchView, self).get_context_data(object_list=None, **kwargs)
        # Get the app configuration for the specified app
        app_config = apps.get_app_config('organization')
        # Get all models from the specified app
        app_models = app_config.get_models()
        # Name of the model to exclude
        model_to_exclude = 'BasicOrgInfo'
        # Filter models excluding the one specified
        filtered_models = [model for model in app_models if model.__name__ != model_to_exclude]

        applicant_units = []
        owner_unit_options = []

        for md in self.get_queryset():
            # Now, app_models is a list of model classes in the 'organization' app
            for model in filtered_models:
                try:
                    applicant_units.append(model.objects.get(id=md.applicant_unit_object_id))
                    break
                except ObjectDoesNotExist:
                    pass
        context['certificate_applications'] = zip(self.get_queryset(), applicant_units)
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
