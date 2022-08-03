from booking import views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.BookingEnquiry.as_view(), name='booking'),
    path('manage_booking', views.ManageBooking.as_view(),
         name='manage_booking'),
    path('edit_booking/<booking_id>', views.EditBooking.as_view(),
         name='edit_booking'),
    path('delete_booking/<booking_id>',
         views.DeleteBooking.as_view(), name='delete_booking'),
    ]
