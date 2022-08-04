from datetime import date
from django import forms
from django.conf import settings
from .models import Customer, Booking


today = date.today()


class CustomerForm(forms.ModelForm):
    """ The Customer Form Model """
    email = forms.EmailField(required=True)

    class Meta:
        """Custome Field Form """
        model = Customer
        fields = ('full_name', 'email')


class BookingForm(forms.ModelForm):
    """ The Booking Form Model """
    requested_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMAT)

    class Meta:
        """Booking form field"""
        model = Booking
        fields = ('class_name', 'requested_date')
