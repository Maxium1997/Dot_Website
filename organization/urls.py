from django.urls import path, include
# from .views import ExportOrganizationToCSV
from .views import OrganizationView
from .views import download_unit_template, upload_units

urlpatterns = [
    # other patterns...
    # path('export-organization-data/', ExportOrganizationToCSV.as_view(), name='export_organization_data'),
    path('Organization', OrganizationView.as_view(), name='organization'),
    path('Organization/', include([
        path('download_unit_template', download_unit_template, name='download_unit_template'),
        path('upload_units', upload_units, name='upload_units'),
    ])),
]
