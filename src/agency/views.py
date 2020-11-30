from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
import datetime

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string
from .forms import CountrySearchForm, DepartureCitySearchForm, DepartureDateForm,  NightAmountForm, CitySearchForm, HotelSearchForm, UploadFileForm
from .tasks import regular_backup_database, task_hello, task_export_db_to_excel
from .service import get_countries, get_available_tours, get_country_cities, get_cities_hotels, get_country_hotels, create_order, get_tour_by_id, get_tour_hotel_by_id, export_models_to_excel, save_excel_book_to_database
import logging

logger = logging.getLogger(__name__)


def index(request):
    
    proposed_departure_date = datetime.date.today() + datetime.timedelta(days=2)
    departure_date_form = DepartureDateForm(initial={'departure_date': proposed_departure_date,})
    country_search_form = CountrySearchForm()
    city_search_form = CitySearchForm()
    hotel_search_form = HotelSearchForm()
    departure_city_search_form = DepartureCitySearchForm()
    night_amount_form = NightAmountForm()
    
    return render(request, 'base.html', {
        'departure_date_form': departure_date_form, 
        'country_search_form': country_search_form,
        'departure_city_search_form': departure_city_search_form,
        'night_amount_form': night_amount_form,
        'city_search_form': city_search_form,
        'hotel_search_form': hotel_search_form,
        })


def ajax_get_available_tours(request):
    data = dict()
    if request.method == 'POST':
        logger.info(request.POST)
        tours = get_available_tours(
            request.POST.get('country'),
            request.POST.getlist('city[]'),
            request.POST.getlist('hotel[]'),
            request.POST.get('departure_date'),
            request.POST.get('night_count'),
            request.POST.get('departure_city'),
        )
        data['html_available_tours'] = render_to_string("available_tours.html", {'tours': tours}, request)
        # return render(request, "available_tours.html", {tours})
        return JsonResponse(data)


def load_cities(request):
    cities = get_country_cities(request.GET.get('country'))
    return render(request, 'dropdown/city_dropdown_list_options.html', {'cities': cities})


def load_hotels(request):
    cities = request.GET.get('city')
    if len(cities) > 0:
        cities = str(cities).split(',')
        hotels = get_cities_hotels(cities)
    else:
        hotels = None
    return render(request, 'dropdown/hotel_dropdown_list_options.html', {'hotels': hotels})


def load_country_hotels(request):
    hotels = get_country_hotels(request.GET.get('country'))
    return render(request, 'dropdown/hotel_dropdown_list_options.html', {'hotels': hotels})


def ajax_create_order(request):
    
    if request.method == "GET":
        tour = get_tour_by_id( request.GET.get('tour'))
        tour_hotel = get_tour_hotel_by_id(request.GET.get('tour-hotel'))
        return render(request, 'create_order.html', {'tour': tour, 'tour_hotel':tour_hotel})
    elif request.method == "POST":
        tour = request.POST.get('tour')
        tour_hotel = request.POST.get('tour-hotel')
        client_name = request.POST.get('client-name')
        client_phone = request.POST.get('client-phone')
        created = create_order(tour, tour_hotel, client_name, client_phone, request.user)
        return render(request, 'create_order_success.html', {'client_name':client_name, 'client_phone':client_phone, 'created':created})


def show_admin_excel_functions(request):
    return render(request, 'admin/excel-functionality.html')


def export_to_excel(request):
    # return task_export_db_to_excel.delay()
    return export_models_to_excel()


def import_data_from_excel(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            save_excel_book_to_database(file=request.FILES["file"])
            return HttpResponse('OK')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(request, 'admin/excel-functionality.html', {'form':form})