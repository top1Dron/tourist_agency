from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
import logging

from .models import Tour, Country, City, DepartureCity, Hotel
from .service import get_countries, get_country_cities, get_departure_cities


logger = logging.getLogger(__name__)


class CountrySearchForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=get_countries(), label='Куди', required=False, blank=True)

    class Meta:
        model = Country
        fields = ('name',)


class CitySearchForm(forms.ModelForm):
    name = forms.ModelMultipleChoiceField(queryset=City.objects.none(), required=False)

    class Meta:
        model = City
        fields = ('name',)
        widget = {
            'name': forms.SelectMultiple
        }


class HotelSearchForm(forms.ModelForm):
    name = forms.ModelMultipleChoiceField(
        queryset=Hotel.objects.none(),initial=0, label='Куди', 
        widget = forms.SelectMultiple, required=False
    )

    class Meta:
        model = Hotel
        fields = ('name',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].queryset = Hotel.objects.none()


class DepartureCitySearchForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=get_departure_cities(), initial=1, label='Звідки')

    class Meta:
        model = DepartureCity
        fields = ('name',)


class DepartureDateForm(forms.Form):

    departure_date = forms.DateField(label='Дата вильоту')

    def clean_renewal_date(self):
        data = self.cleaned_data['departure_date']
        
        #Check that date isn`t in the past
        if data < datetime.date.today():
            raise ValidationError(_('Дата відправлення не може бути у минулому!'))


        return data

    
class NightAmountForm(forms.Form):

    night = forms.IntegerField(label='До скількох ночей?', max_value=21, min_value=1, initial=5)


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл')

# class CreateOrderForm(forms.Form):
#     client_name = forms.TextInput(label_suffix='Ваше ПІБ:', max_length=128, required=True)
#     client_phone_number = forms.TextInput(attrs={'class': 'form-control bfh-phone'}), max_length=128, required=True, label="Ваш телефон:")


# COUNTRIES = get_countries()


# class SearchTourForm(forms.Form):
#     # fields = ['country', 'departure_date', 'tour_type', 'departure_city']
#     country = forms.ChoiceField(choices=COUNTRIES, initial='0', required=True)
#     city = forms.ChoiceField(choices=[get_country_cities(-1)], required=True)


#     def __init__(self, *args, **kwargs):
#         logger.info(COUNTRIES)
#         super().__init__(*args, **kwargs)