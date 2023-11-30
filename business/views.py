from django.shortcuts import render
from django.views.generic import TemplateView, ListView
# from django.http import HttpResponse
# import pandas as pd
# from openpyxl import Workbook
# from openpyxl.writer.excel import save_virtual_workbook


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


from django.http import HttpResponse
from openpyxl import Workbook

def export_all(request):
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
