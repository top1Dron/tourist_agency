# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdditionalService(models.Model):
    name = models.TextField()  # This field type is a guess.
    cost = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'additional_service'
        verbose_name = "Додаткова послуга"
        verbose_name_plural = "Додаткові послуги"


class City(models.Model):
    name = models.CharField(unique=True, max_length=40)
    country = models.ForeignKey('Country', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'city'
        verbose_name = "Місто"
        verbose_name_plural = "Міста"


    def __str__(self):
        return f'{self.name}'


class Client(models.Model):
    full_name = models.CharField(db_column='full name', max_length=60)  # Field renamed to remove unsuitable characters.
    phone_number = models.CharField(unique=True, max_length=18)

    class Meta:
        managed = False
        db_table = 'client'
        verbose_name = "Клієнт"
        verbose_name_plural = "Клієнти"


class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'country'
        verbose_name = "Країна"
        verbose_name_plural = "Країни"


    def __str__(self):
        return self.name
    


class DepartureCity(models.Model):
    name = models.CharField(unique=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'departure_city'
        verbose_name = "Місто відправлення"
        verbose_name_plural = "Міста відправлення"


    def __str__(self):
        return self.name
    

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)
    stars = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'hotel'
        verbose_name = "Готель"
        verbose_name_plural = "Готелі"


    def __str__(self):
        return f'{self.name} {self.stars}* ({self.city}, {self.city.country})'


    @property
    def to_string(self):
        return f'{self.name} {self.stars}*'


class Order(models.Model):
    client = models.ForeignKey(Client, models.DO_NOTHING)
    tour = models.ForeignKey('Tour', models.DO_NOTHING)
    clearance_date = models.DateField(db_column='clearance date')  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'order'
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"


    def __str__(self):
        return f'Order for tour:{self.tour} by {self.client}. Clearance date:{self.clearance_date}'
    


class OrderService(models.Model):
    order = models.ForeignKey(Order, models.DO_NOTHING)
    service = models.ForeignKey(AdditionalService, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'order_service'
        verbose_name = "Додаткова послуга в замовленні"
        verbose_name_plural = "Додаткові послуги в замовленнях"


class Staff(models.Model):
    full_name = models.CharField(max_length=120)
    birthday_date = models.DateField()
    salary = models.IntegerField()
    position = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=18)

    class Meta:
        managed = False
        db_table = 'staff'
        verbose_name = "Службовий персонал"
        verbose_name_plural = "Службовий персонал"


class StaffTour(models.Model):
    staff = models.ForeignKey(Staff, models.DO_NOTHING)
    tour = models.ForeignKey('Tour', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'staff_tour'
        verbose_name = "Службовий персоналу турі"
        verbose_name_plural = "Службовий персонал у турах"


class Tour(models.Model):
    transport = models.ForeignKey('Transport', models.DO_NOTHING, blank=True, null=True)
    tour_type = models.ForeignKey('TourType', models.DO_NOTHING)
    departure_date = models.DateTimeField()
    return_date = models.DateTimeField()
    country = models.ForeignKey(Country, models.DO_NOTHING, blank=True, null=True)
    departure_city = models.ForeignKey(DepartureCity, models.DO_NOTHING)
    nights = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tour'
        verbose_name = "Тур"
        verbose_name_plural = "Тури"


    def __str__(self):
        return f'{self.pk}'


    def get_tour_cities(self):
        return TourCity.objects.filter(tour=self.pk)


    def get_tour_hotels(self):
        return TourHotel.objects.filter(tour=self.pk)


class TourCity(models.Model):
    tour = models.ForeignKey(Tour, models.DO_NOTHING)
    city = models.ForeignKey(City, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tour_city'
        verbose_name = "Міста у турі"
        verbose_name_plural = "Міста у турах"


    def __str__(self):
        return f'{self.tour}'


class TourHotel(models.Model):
    tour = models.ForeignKey(Tour, models.CASCADE)
    hotel = models.ForeignKey(Hotel, models.CASCADE)
    tour_cost = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tour_hotel'
        verbose_name = "Готель у турі"
        verbose_name_plural = "Готелі у турах"


    def __str__(self):
        return f'{self.tour}'


class TourType(models.Model):
    name = models.CharField(unique=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'tour_type'
        verbose_name = "Тип туру"
        verbose_name_plural = "Типи турів"


    def __str__(self):
        return f'{self.name}'


class Transport(models.Model):
    name = models.CharField(unique=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'transport'
        verbose_name = "Транспорт"
        verbose_name_plural = "Транспорт"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class UsersCustomuser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    email = models.CharField(unique=True, max_length=254)

    class Meta:
        managed = False
        db_table = 'users_customuser'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'