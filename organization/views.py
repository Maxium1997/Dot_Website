from django.shortcuts import render

from openpyxl import Workbook

import csv
from django.http import HttpResponse
from django.views.generic import View
from .models import Administration, Branch, PatrolAreaOffice, Brigade, CoastPatrolCorps, InternalUnit, PatrolStation, \
    InspectionOffice


# Create your views here.

class ExportOrganizationToCSV(View):
    def get(self, request, *args, **kwargs):
        # Get querysets for all relevant models
        administrations = Administration.objects.all()
        branches = Branch.objects.all()
        patrol_area_offices = PatrolAreaOffice.objects.all()
        brigades = Brigade.objects.all()
        coast_patrol_corps = CoastPatrolCorps.objects.all()
        internal_units = InternalUnit.objects.all()
        patrol_stations = PatrolStation.objects.all()
        inspection_offices = InspectionOffice.objects.all()

        # Create a response object with CSV content
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="organizations_data.csv"'

        # Define a dictionary to map models to their respective querysets and field headers
        models_data = {
            'Administration': (administrations, ['name', 'en_name', 'director', 'deputy_director1', 'deputy_director2', 'deputy_director3', 'address', 'landline_phone', 'email']),
            'Branch': (branches, ['name', 'en_name', 'director', 'deputy_director1', 'deputy_director2', 'deputy_director3', 'address', 'landline_phone', 'superior']),
            'PatrolAreaOffice': (patrol_area_offices, ['name', 'en_name', 'director', 'deputy_director1', 'deputy_director2', 'deputy_director3', 'number', 'superior', 'dispatch', 'administrative_region']),
            'Brigade': (brigades, ['name', 'en_name', 'director', 'deputy_director1', 'deputy_director2', 'deputy_director3', 'number', 'superior', 'garrison']),
            'CoastPatrolCorps': (coast_patrol_corps, ['name', 'en_name', 'director', 'deputy_director1', 'deputy_director2', 'deputy_director3', 'address', 'landline_phone', 'central_exchange_intercom', 'superior']),
            'InternalUnit': (internal_units, ['name', 'en_name', 'director', 'deputy_director1', 'deputy_director2', 'deputy_director3', 'serial_number', 'superior']),
            'PatrolStation': (patrol_stations, ['name', 'en_name', 'director', 'deputy_director1', 'deputy_director2', 'deputy_director3', 'number', 'address', 'landline_phone', 'intercom_phone', 'email', 'superior']),
            'InspectionOffice': (inspection_offices, ['name', 'en_name', 'director', 'deputy_director1', 'deputy_director2', 'deputy_director3', 'address', 'landline_phone', 'intercom_phone', 'email', 'superior']),
        }

        # Write data for each model to the CSV file
        for model_name, (model_queryset, field_headers) in models_data.items():
            csv_writer = csv.writer(response)
            csv_writer.writerow([f'{model_name} Data'])
            csv_writer.writerow(field_headers)

            for instance in model_queryset:
                csv_writer.writerow([getattr(instance, field) for field in field_headers])

            # Add a newline to separate worksheets
            response.write('\n')

        return response


