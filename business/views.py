from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse
from django.db import IntegrityError
from django.db.models import Q
from django.apps import apps
from django.views.generic import TemplateView, ListView
from openpyxl import Workbook
import pandas as pd
# from openpyxl.writer.excel import save_virtual_workbook


from .models import MobileStorageEquipment, MobileDevice, CertificateApplication
from organization.models import *
from organization.definitions import CPC4Unit, ArmyCommission

# Create your views here.


class BusinessView(TemplateView):
    template_name = 'business/index.html'


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


def export_mse_all(request):
    # Get queryset data
    queryset = MobileStorageEquipment.objects.all()

    # Create a workbook and add a worksheet
    wb = Workbook()
    ws = wb.active

    # Write the header row
    header = ["Serial Number", "Name", "Built-in Memory", "Brand", "Type", "Model", "Capacity",
              "Storage Unit", "Manage Unit", "Manager", "Deputy Manager", "Remarks"]
    ws.append(header)

    # Write data rows
    for item in queryset:
        row_data = [
            item.serial_number, item.name, item.builtin_memory, item.brand,
            item.get_type_display(), item.model, item.capacity,
            item.get_storage_unit_display(), item.get_manage_unit_display(),
            item.manager, item.deputy_manager, item.remarks
        ]
        ws.append(row_data)

    # Create a response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=mobile_storage_equipment.xlsx'

    # Save the workbook directly to the response
    wb.save(response)

    return response


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


def process_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']

        # 讀取 Excel 文件
        df = pd.read_excel(excel_file)
        # excel_data = ['#', 'owner_unit', 'commission', 'owner', 'SP_brand', 'SP_model', 'SW_brand', 'SW_model']
        excel_data = []
        for index, row in df.iterrows():
            # 將每一行的數據轉換為字典
            row_data = row.to_dict()
            excel_data.append(row_data)

        query_exists = []
        query_creates = []
        for data in excel_data:
            try:
                query_exists.append(MobileDevice.objects.get(owner=data.get('owner')))
            except IntegrityError:
                break
            except:
                cpc4_units = {_.value[2]: _.value[0] for _ in CPC4Unit.__members__.values()}
                data_owner_unit = data.get('unit')
                get_owner_unit = cpc4_units.get(data_owner_unit)

                try:
                    commissions = {_.value[2]: _.value[0] for _ in ArmyCommission.__members__.values()}
                    data_owner_commission = data.get('owner_commission')
                    get_owner_commission = commissions.get(data_owner_commission)
                except:
                    get_owner_commission = ArmyCommission.NonSet.value[0]

                mobile_device = MobileDevice(
                    owner=data.get('owner'),
                    owner_unit=get_owner_unit,
                    owner_commission=get_owner_commission,
                    SP_brand=data.get('SP_brand'),
                    SP_model=data.get('SP_model'),
                    SW_brand=data.get('SW_brand'),
                    SW_model=data.get('SW_model'),
                    number=data.get('number')
                )
                mobile_device.save()
                query_creates.append(mobile_device)

        # 傳遞讀取結果到 template2
        return render(request, 'business/MobileDevice/import_result.html', {'excel_data': excel_data,
                                                                            'query_exists': query_exists,
                                                                            'query_creates': query_creates,})

    return render(request, 'business/MobileDevice/import.html')


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
