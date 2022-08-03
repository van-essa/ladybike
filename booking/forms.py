from .models import Customer, Booking
from django import forms
from datetime import date


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
    requested_date = forms.DateField(widget=forms.TextInput
    (attrs={'min': today, 'value': today, 'type': 'date'}), required=True)

    class Meta:
        """Booking form field"""
        model = Booking
        fields = ('class_name', 'requested_date')
