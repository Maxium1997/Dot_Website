from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from openpyxl import Workbook
# import pandas as pd
# from openpyxl.writer.excel import save_virtual_workbook


from .models import MobileStorageEquipment, MobileDevice
from organization.definitions import CPC4Unit

# Create your views here.


class BusinessView(TemplateView):
    template_name = 'business/index.html'


class MobileStorageEquipmentView(ListView):
    model = MobileStorageEquipment
    template_name = 'business/MobileStorageEquipment/all.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MobileStorageEquipmentView, self).get_context_data(object_list=None, **kwargs)
        context['mobile_storage_equipments'] = MobileStorageEquipment.objects.all().order_by('manage_unit')
        context['manage_units'] = [(_.value[0], _.value[2]) for _ in CPC4Unit.__members__.values()]
        return context


class MobileStorageEquipmentFilteredView(ListView):
    template_name = 'business/MobileStorageEquipment/filtered.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MobileStorageEquipmentFilteredView, self).get_context_data(object_list=None, **kwargs)
        manage_unit = self.request.GET.get('manage_unit')
        if manage_unit == "":
            context['manage_unit'] = ""
        else:
            context['manage_unit'] = int(self.request.GET.get('manage_unit'))

        context['mobile_storage_equipments'] = self.get_queryset()
        context['manage_units'] = [(_.value[0], _.value[2]) for _ in CPC4Unit.__members__.values()]
        return context

    def get_queryset(self):
        manage_unit = self.request.GET.get('manage_unit')
        if manage_unit == "":
            return MobileStorageEquipment.objects.all()
        else:
            return MobileStorageEquipment.objects.filter(manage_unit=manage_unit)


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
        context['mobile_devices'] = self.get_queryset()
        # context['manage_units'] = [(_.value[0], _.value[2]) for _ in CPC4Unit.__members__.values()]
        return context

    def get_queryset(self):
        return MobileDevice.objects.all()


# views.py
from django.shortcuts import render
import pandas as pd


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

        # 傳遞讀取結果到 template2
        return render(request, 'business/MobileDevice/import_result.html', {'excel_data': excel_data})

    return render(request, 'business/MobileDevice/import.html')

