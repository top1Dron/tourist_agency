import logging
logger = logging.getLogger(__name__)


from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import AdditionalService, City, Client, \
    Country, DepartureCity, Hotel, Order, OrderService, \
        Staff, StaffTour, Tour, TourCity, TourHotel, TourType, Transport


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        # if obj.action_flag == DELETION:
        #     link = escape(obj.object_repr)
        # else:
        ct = obj.content_type
        link = '<a href="%s">%s</a>' % (
            reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
            escape(obj.object_repr),
        )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"


@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cost')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(DepartureCity)
class DepartureCityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'stars')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'tour', 'clearance_date')


@admin.register(OrderService)
class OrderServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'service')


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'birthday_date', 'salary', 'position', 'phone_number')


@admin.register(StaffTour)
class StaffTourAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'tour')


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('id', 'transport', 'tour_type', 'departure_date', 'return_date', 'country', 'departure_city', 'nights')


@admin.register(TourCity)
class TourCityAdmin(admin.ModelAdmin):
    list_display = ('id', 'tour', 'city')


@admin.register(TourHotel)
class TourHotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'tour', 'hotel', 'tour_cost')


@admin.register(TourType)
class TourTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')