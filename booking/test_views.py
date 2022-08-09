"""Imports"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from booking.models import Customer, ClassName, Booking


class TestBookingViews(TestCase):
    """Test views"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='project.test@test.com',
            email='project.test@test.com', password='12345')
        self.client.login(
            username='project.test@test.com',
            email='project.test@test.com', password='12345')
        self.booking_url = reverse('booking')
        self.manage_booking_url = reverse('manage_booking')

        self.classname = ClassName.objects.create(
            classes=1
        )

        self.customer = Customer.objects.create(
            customer_id=1,
            full_name='Project Test',
            email='project.test@test.com'
        )

        self.booking1 = Booking.objects.create(
            booking_id=32,
            customer=self.customer,
            class_name=self.classname,
            status='Available',
            seats=1,
            requested_date='2022-09-23',
            bookingtatus='p'
        )

        self.booking2 = Booking.objects.create(
            booking_id=42,
            customer=self.customer,
            class_name=self.classname,
            status='Available',
            seats=2,
            requested_date='2022-10-29',
            bookingtatus='p'
        )

        self.edit_booking1_url = reverse('edit_booking', args=[32])
        self.delete_booking1_url = reverse('delete_booking', args=[32])
        self.edit_booking2_url = reverse('edit_booking', args=[42])
        self.delete_booking2_url = reverse('delete_booking', args=[42])

    def test_booking_GET(self):
        """test booking"""
        response = self.client.get(self.booking_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking.html')

    def test_manage_booking_GET(self):
        """test manage booking"""
        response = self.client.get(self.manage_booking_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_booking.html')

    def test_manage_booking_GET_unathorised_user_redirected(self):
        """test booking and auth"""
        self.client.logout()
        response = self.client.get(self.manage_booking_url)

        self.assertEquals(response.status_code, 302)

    def test_delete_booking_GET(self):
        """test delete booking"""
        response = self.client.get(self.delete_booking_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_booking.html')

    def test_delete_booking_GET_unathorised_user_redirected(self):
        """test delete booking and auth"""
        self.client.logout()
        response = self.client.get(self.delete_booking1_url)

        self.assertEquals(response.status_code, 302)

    def test_edit_booking_GET(self):
        """test edit booking"""
        response = self.client.get(self.edit_booking1_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_booking.html')

    def test_edit_booking_GET_unathorised_user_redirected(self):
        """test edit booking and auth"""
        self.client.logout()
        response = self.client.get(self.edit_booking1_url)

        self.assertEquals(response.status_code, 302)

    def test_delete_booking_GET_date_in_past_redirected(self):
        """test delet booking and past date"""
        response = self.client.get(self.delete_booking2_url)

        self.assertEquals(response.status_code, 302)

    def test_edit_booking_GET_date_in_past_redirected(self):
        """test delet booking and past date"""
        response = self.client.get(self.edit_booking2_url)

        self.assertEquals(response.status_code, 302)

    def test_booking_POST_adds_new_customer_and_booking(self):
        """test booking and customer post"""
        class_name = self.classname

        customer = Customer.objects.create(
            customer_id=3,
            full_name='Project Test123',
            email='project.test123@test.com'
        )

        booking = Booking.objects.create(
            booking_id=36,
            customer=self.customer,
            class_name=self.classname,
            status='Available',
            seats=3,
            requested_date='2022-12-29',
            bookingtatus='p'
        )

        response = self.client.post(self.booking_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(Booking.objects.all()), 3)
        self.assertEquals(len(Customer.objects.all()), 2)

    def test_booking_POST_does_not_add_customer_that_exists(self):
        """test booking and customer"""
        class_name = self.classname
        customer = self.customer
        booking = Booking.objects.create(
            booking_id=39,
            customer=self.customer,
            class_name=self.classname,
            status='Available',
            seats=3,
            requested_date='2022-12-01',
            bookingtatus='p'
        )

        response = self.client.post(self.booking_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(Booking.objects.all()), 3)
        self.assertEquals(len(Customer.objects.all()), 1)

    def test_edit_booking_POST_updates_model(self):
        """test edit booking and update"""
        booking = self.booking1

        booking.requested_date = '2022-11-01'

        response = self.client.post(self.edit_booking1_url)

        self.assertEquals(self.booking1.requested_date, '2022-11-01')

    def test_delete_booking_POST_updates_model(self):
        """test delete booking and update"""
        booking = self.booking2
        response = self.client.post(self.delete_booking2_url)

        self.assertEquals(len(Booking.objects.all()), 1)
        self.assertNotIn(self.booking2, Booking.objects.all())