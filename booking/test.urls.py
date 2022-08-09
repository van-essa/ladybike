"""Imports"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from booking.views import (
    BookingEnquiry, ManageBooking, EditBooking, DeleteBooking)


# Create your tests here
class TestReservationsUrls(SimpleTestCase):
    """Test Urls"""
    def test_booking_url_is_resolved(self):
        """Test Booking url"""
        url = reverse('booking')
        self.assertEquals(resolve(url).func.view_class, BookingEnquiry)

    def test_manage_booking_url_is_resolved(self):
        """Test Manage Booking url"""
        url = reverse('manage_booking')
        self.assertEquals(resolve(url).func.view_class, ManageBooking)

    def test_edit_booking_url_is_resolved(self):
        """Test Edit Booking url"""
        url = reverse('edit_booking', args=['booking_id'])
        self.assertEquals(resolve(url).func.view_class, EditBooking)

    def test_delete_booking_url_is_resolved(self):
        """Test Delete Booking url"""
        url = reverse('delete_booking', args=['booking_id'])
        self.assertEquals(resolve(url).func.view_class, DeleteBooking)
