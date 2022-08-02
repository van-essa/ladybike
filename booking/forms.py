from .models import Customer, Booking
from django import forms
from django.conf import settings


class CustomerForm(forms.ModelForm):
    """ The Customer Form Model """
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Customer
        fields = ('full_name', 'email', 'password')


class BookingForm(forms.ModelForm):
    """ The Booking Form Model """
    requested_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMAT)

    class Meta:
        model = Booking
        fields = ('class_name', 'requested_date')