"""Imports"""
from django.test import TestCase
from booking.models import Booking, ClassName, Customer


class TestBookingModels(TestCase):
    """Test Booking Models"""

    def setUp(self):
        self.classname = ClassName(classes=1)
        self.customer = Customer(
            customer_id=12, full_name='Test 123', email='test123@gmail.com')
        self.booking = Booking(
            booking_id=32,
            customer=self.customer,
            class_name=self.classname,
            status='Available',
            seats=1,
            requested_date='2022-01-23',
            bookingtatus='p')

    def test_create_classname(self):
        """Test ClassName"""
        self.assertEqual(self.classname.classes, 1)

    def test_create_customer(self):
        """Test Customer"""
        self.assertEqual(self.customer.customer_id, 12)
        self.assertEquals(self.customer.full_name, 'Test 123')
        self.assertEquals(self.customer.email, 'test123@gmail.com')

    def test_create_booking(self):
        """Test Booing"""
        self.assertEqual(self.booking.booking_id, 32)
        self.assertEquals(self.booking.customer, self.customer)
        self.assertEquals(self.booking.class_name, self.classname)
        self.assertEquals(self.booking.status, 'Available')
        self.assertEquals(self.booking.seats, 4)
        self.assertEquals(self.booking.requested_date, '2022-09-23')
        self.assertEquals(self.booking.bookingtatus, 'p')

    def test_customer_on_delete_cascade_works(self):
        """Test cstomer on delete"""
        customer = self.customer
        customer.delete()

        booking = len(Booking.objects.all())
        self.assertEquals(booking, 0)

    def test_class_name_on_delete_cascade_works(self):
        """Test on delete class name"""
        class_name = self.classname
        class_name.delete()

        booking = len(Booking.objects.all())
        self.assertEquals(booking, 0)
