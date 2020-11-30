import datetime
from datetime import datetime as dt
from django.core.management import call_command
from django.conf import settings
from django.db import connection
import logging
import django_excel as excel
import os
from pyexcel.exceptions import FileTypeNotSupported
from .models import AdditionalService, City, Client, \
    Country, DepartureCity, Hotel, Order, OrderService, \
        Staff, StaffTour, Tour, TourCity, TourHotel, TourType, \
            Transport, DjangoAdminLog, DjangoContentType, UsersCustomuser


logger = logging.getLogger(__name__)

# logging.disable(logging.INFO)

def backup_database():
    try:
        call_command('dbbackup')
        logger.info(f'Created database backup at {dt.now().strftime("%Y-%m-%d--%H-%M-%S")}')
    except:
        logger.info(f'Error in creation of database backup at {dt.now().strftime("%Y-%m-%d--%H-%M-%S")}')


def print_message(message):
    logger.info(f'{message}')


def custom_backup_db():
    time = dt.now().strftime("%Y-%m-%d-%H%M%S")
    DB_NAME = 'tourist_agency'
    DB_USER = 'admin'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_PASSWORD = 'top1Dron'
    DB_BACKUP_FILE_NAME = f'default-{DB_USER}-{time}.psql'
    
    dump_success = 1
    logger.info(f'Backing up {DB_NAME} database')
    logger.info(os.environ['PG_DUMP'])
    command_for_dumping = f'{os.environ["PG_DUMP"]} ' \
                f'-h {DB_HOST} ' \
                f'-U {DB_USER} ' \
                f'{DB_NAME} ' \
                f'> "{os.path.join(settings.BACKUP_DIR, DB_BACKUP_FILE_NAME)}"'
    logger.info(command_for_dumping)
    try:
        proc = subprocess.Popen(command_for_dumping, shell=True, env={
                    'PGPASSWORD': f'{DB_PASSWORD}'
                    })
        proc.wait()

    except Exception as e:
            dump_success = 0
            logger.info('Exception happened during dump %s' %(e))


    if dump_success:
        logger.info('db dump successfull')


def export_models_to_excel():
    responce = None
    
    EXCEL_FILE_NAME = dt.now().strftime("%Y-%m-%d-%H%M%S") + '-tourist_agency'
    try:
        responce = excel.make_response_from_tables([
            City, Client, Country, DepartureCity, Hotel, 
            Order, OrderService, Staff, StaffTour, TourHotel,
            Tour, TourCity, TourType, Transport], 'xlsx', file_name=EXCEL_FILE_NAME)
        logger.info('Export database to excel finished successfully')
    except Exception as error:
        logger.info(f'Export database to excel failed: {str(error)}')
    return responce


def save_excel_book_to_database(file):
    def city_check(row):
        city = City.objects.filter(name=row[1])
        if city.exists() == True:
            return None
        else:
            country = Country.objects.filter(id=row[0])[0]
            row[0] = country
        return row

    def country_check(row):
        country = Country.objects.filter(name=row[0])
        if country.exists() == True:
            return None
        else:
            return row
    
    file.save_book_to_database(
        models=[ City, Client, Country, DepartureCity, Hotel, 
            Order, OrderService, Staff, StaffTour, TourHotel,
            Tour, TourCity, TourType, Transport],
        initializers=[city_check, None, country_check, None, None,None, None,None, None,None, None,None, None,None],
        mapdicts=[
            {"country_id":'country', "name":'name'},
            {'full_name':'full_name', 'phone_number': 'phone_number'},
            {'name':'name'},
            {'name':'name'},
            {'name':'name', 'city_id':'city', 'stars':'stars'},
            {'client_id':'client', 'clearance_date':'clearance_date', 'tour_id':'tour'},
            {'order_id':'order', 'service_id':'service'},
            {'full_name':'full_name', 'birthday_date':'birthday_date', 'salary':'salary', 'position':'position', 'phone_number':'phone_number'},
            {'staff_id':'staff', 'tour_id':'tour'},
            {'tour_id':'tour', 'hotel_id':'hotel', 'tour_cost':'tour_cost'},
            {'transport_id':'transport', 'tour_type_id':'tour_type', 'departure_date':'departure_date', 'return_date':'return_date', 'country_id':'country', 'departure_city_id':'departure_city', 'nights':'nights'},
            {'city_id':'city', 'tour_id':'tour'},
            {'name':'name'},
            {'name':'name'},
        ],
    )


def get_countries():
    return Country.objects.all()


def get_departure_cities():
    return DepartureCity.objects.all()


def get_country_cities(country_id):
    return City.objects.filter(country=country_id).order_by("name")


def get_cities_hotels(cities):
    return Hotel.objects.filter(city__in=cities).order_by("name")


def get_country_hotels(country_id):
    cities = get_country_cities(country_id)
    return get_cities_hotels(cities)


def get_available_tours(country, cities, hotels, departure_date, night_count, departure_city):
    available_tours = Tour.objects.all()
    logger.info(available_tours)
    if len(departure_date) > 0:
        if '-' in departure_date:
            departure_date = f'{departure_date[-2]}{departure_date[-1]}.{departure_date[-5]}{departure_date[-4]}.{departure_date[0]}{departure_date[1]}{departure_date[2]}{departure_date[3]}'
        departure_date = [int(_) for _ in departure_date.split('.')]
        available_tours = available_tours \
            .filter(departure_date__date=datetime.date(departure_date[2], departure_date[1], departure_date[0]))
        logger.info(f'{available_tours} - filter departure_date')

    if len(night_count) > 0:
        available_tours = available_tours.filter(nights=night_count)
        logger.info(f"{available_tours} - filter night_count")

    if len(departure_city) > 0:
        available_tours = available_tours.filter(departure_city=departure_city)
        logger.info(f"{available_tours} - filter departure_city")
    
    if len(country) > 0:
        available_tours = available_tours.filter(country=country)
        logger.info(f"{available_tours} - filter country")
        if len(cities) > 0 and cities[0] != '' and len(hotels) == 1 and hotels[-1] == '':
            available_tours = TourCity.objects.filter(tour__in=available_tours).filter(city__in=cities)
            available_tours = Tour.objects.filter(pk__in=[tour_city.tour.id for tour_city in available_tours])
            logger.info(f"{available_tours} - filter cities")
        elif len(hotels) > 0 and hotels[0] != '' and len(cities) == 1 and cities[-1] == '':
            # cities = City.objects.filter(hotel__in=Hotel.objects.filter(pk__in=hotels))
            available_tours = TourHotel.objects.filter(tour__in=available_tours).filter(hotel__in=Hotel.objects.filter(pk__in=hotels))
            
            logger.info(f'{available_tours.query}')
            available_tours = Tour.objects.filter(pk__in=[tour_hotel.tour.id for tour_hotel in available_tours])
            if available_tours.exists():
                logger.info(f"{available_tours} - filter hotels\n{available_tours.query}")
        elif len(hotels) > 0 and hotels[0] != '' and len(cities) > 0 and cities[0] != '':
            available_tours = TourHotel.objects.filter(tour__in=available_tours).filter(hotel__in=Hotel.objects.filter(pk__in=hotels))
            if available_tours.exists():
                logger.info(f'{available_tours.query}')
            available_tours = Tour.objects.filter(pk__in=[tour_hotel.tour.id for tour_hotel in available_tours])
            if available_tours.exists():
                logger.info(f"{available_tours} - filter hotels\n{available_tours.query}")
    logger.info(f"{available_tours} - end filter")
    return available_tours


def create_order(_tour_id, _tour_hotel_id, _client_fullname, _client_phonenumber, user='guest'):

    cursor = connection.cursor()
    try:
        cursor.execute(f"CALL create_order( {int(_tour_id)}, {int(_tour_hotel_id)}, '{_client_fullname}'::VARCHAR, '{_client_phonenumber}'::VARCHAR, '{str(datetime.date.today())}'::VARCHAR);")
        logger.info('Procedure create_order executed successful')
    except Exception as e:
        logger.error(f'create_order procedure execution failed. Exception: {e}')
        return False
    finally:
        cursor.close()
    
    try:
        if f'{user}' == 'AnonymousUser':
            user = UsersCustomuser.objects.get(id=2)
        else:
            user = UsersCustomuser.objects.get(email=user.email)
        DjangoAdminLog.objects.create(action_time=dt.now(),object_id=Order.objects.all().order_by("-id")[0], object_repr=f'Added order {Order.objects.all().order_by("-id")[0]}.', action_flag=1, change_message='', content_type=DjangoContentType.objects.get(id=6), user=user)
    except ValueError as val_err:
        logger.error(f'Exception at logging. {e}')
    return True


def get_tour_by_id(tour_id:int) -> Tour:
    try:
        return Tour.objects.get(pk=tour_id)
    except Exception as e:
        logger.error("Tour not found by id.")


def get_tour_hotel_by_id(tour_hotel_id:int) -> TourHotel:
    try:
        return TourHotel.objects.get(pk=tour_hotel_id)
    except Exception as e:
        logger.error("TourHotel not found by id.")