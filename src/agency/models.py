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


    def __str__(self):
        return f'{self.pk} {self.name}'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class City(models.Model):
    name = models.CharField(unique=True, max_length=40)
    country = models.ForeignKey('Country', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'city'


class Client(models.Model):
    full_name = models.CharField(db_column='full name', max_length=60)  # Field renamed to remove unsuitable characters.
    phone_number = models.CharField(unique=True, max_length=18)

    class Meta:
        managed = False
        db_table = 'client'


class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'country'


class DepartureCity(models.Model):
    name = models.CharField(unique=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'departure_city'


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


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)
    stars = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'hotel'


class Order(models.Model):
    client = models.ForeignKey(Client, models.DO_NOTHING)
    tour = models.ForeignKey('Tour', models.DO_NOTHING)
    clearance_date = models.DateField(db_column='clearance date')  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'order'


class OrderService(models.Model):
    order = models.ForeignKey(Order, models.DO_NOTHING)
    service = models.ForeignKey(AdditionalService, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'order_service'


class Staff(models.Model):
    full_name = models.CharField(max_length=120)
    birthday_date = models.DateField()
    salary = models.IntegerField()
    position = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=18)

    class Meta:
        managed = False
        db_table = 'staff'


class StaffTour(models.Model):
    staff = models.ForeignKey(Staff, models.DO_NOTHING)
    tour = models.ForeignKey('Tour', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'staff_tour'


class Tour(models.Model):
    transport = models.ForeignKey('Transport', models.DO_NOTHING, blank=True, null=True)
    tour_type = models.ForeignKey('TourType', models.DO_NOTHING)
    departure_date = models.DateTimeField()
    return_date = models.DateTimeField()
    tour_cost = models.IntegerField()
    country = models.ForeignKey(Country, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tour'


class TourCity(models.Model):
    tour = models.ForeignKey(Tour, models.DO_NOTHING)
    city = models.ForeignKey(City, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tour_city'


class TourType(models.Model):
    name = models.CharField(unique=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'tour_type'


class Transport(models.Model):
    name = models.CharField(unique=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'transport'


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


class UsersCustomuserGroups(models.Model):
    customuser = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_customuser_groups'
        unique_together = (('customuser', 'group'),)


class UsersCustomuserUserPermissions(models.Model):
    customuser = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)
