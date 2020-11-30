from .views import index, ajax_get_available_tours, load_cities, load_hotels, load_country_hotels, ajax_create_order, show_admin_excel_functions, export_to_excel, import_data_from_excel
from django.contrib.auth.decorators import user_passes_test
from django.urls import path

app_name = 'agency'

urlpatterns = [
    path('', index, name='index'),
    path('ajax/find-available-tours', ajax_get_available_tours, name='ajax_find_available_tours'),
    path('ajax/load-cities/', load_cities, name='ajax_load_cities'),
    path('ajax/load-hotels/', load_hotels, name='ajax_load_hotels'),
    path('ajax/load-country-hotels/', load_country_hotels, name='ajax_load_country_hotels'),
    path('ajax/create-order/', ajax_create_order, name='ajax_create_order'),

    path('admin/excel-functions/', user_passes_test(lambda u: u.is_superuser)(import_data_from_excel), name='show_admin_excel_functions'),
    path('admin/export-to-excel/', user_passes_test(lambda u: u.is_superuser)(export_to_excel), name='export_to_excel'),
    path('admin/import-from-excel/', user_passes_test(lambda u: u.is_superuser)(import_data_from_excel), name='import_to_excel'),
]




