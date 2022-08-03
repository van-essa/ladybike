from django.shortcuts import render, reverse, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import ClassName, Customer, Booking
from .forms import CustomerForm, BookingForm
from django.utils.timezone import now
import datetime


# Create your views here.

def classes_urls(request):
    """ Return to classes url """
    return render(request, "classes.html")


def booking_view(request):
    """ Order the data by the date closest to the current \
    date only for dates in the future, not for dates that \
    have passed
    """

    # Show the current and upcoming dates
    today = now().date()
    classes = ClassName.objects.all()
    booking_list = Booking.objects.filter(
        booking_date__gte=today).order_by('requested_date')
    
    return render(request, 'booking.html', {
        'classes': classes, 'booking_list': booking_list})


def get_customer_instance(request, User):
    """ Returns customer instance if User is logged in """
    customer_email = request.user.email
    customer = Customer.objects.filter(email=customer_email).first()

    return customer

    # Counting the amount of classes available that got booked
    def classes_total():
        return Booking.class_name.filter(classstatus='Available').count()

    # Removing the booked seats with the total available seats
    def classes_left():
        return Booking.classes_total - Booking.seats


def check_availabilty(customer_class_name, customer_requested_date):
    """ Check availability against Booking model using customer input """

    # Check to see how many classes exist at that date
    classes_booked = len(float(Booking.objects.filter(
        class_name=customer_class_name,
        requested_date=customer_requested_date, status="Available")))

    # Return number of classes
    return classes_booked


class BookingEnquiry(View):
    """ Booking view allows users to make class enquiries """
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            customer = get_customer_instance(request, User)
            if customer is None:
                email = request.user.email
                customer_form = CustomerForm(initial={'email': email})
            else:
                customer_form = CustomerForm(instance=customer)
            booking_form = BookingForm()

        else:
            customer_form = CustomerForm()
            booking_form = BookingForm()

        return render(request, "booking.html",
                      {'customer_form': customer_form, 'booking_form': booking_form}) 

    def post(self, request, User=User, *args, **kwargs):
        # Get post data from forms
        customer_form = CustomerForm(data=request.POST)
        booking_form = BookingForm(data=request.POST)

        if customer_form.is_valid() and booking_form.is_valid():
            # Fetch information from forms
            customer_class_name = request.POST.get('class_name')
            customer_requested_date = request.POST.get('requested_date')
            customer_name = request.POST.get('full_name')

            # Convert date in to format required by django
            date_formatted = datetime.datetime.strptime(
                customer_requested_date, "%Y-%m-%d").strftime('%d-%m-%Y')

            # Check to see how many bookings exist at that time/date
            classes_booked = check_availabilty(
                customer_requested_date, date_formatted)

            # Get the number of availble seat spot in the classes
            available_seats = classes_left()

            # Compare number of bookings to number of classes available
            if classes_booked >= Booking.seats:
                # If the number of classes booked is bigger
                # than or equal to the max number of classes
                # left in the LadyBike Gym, the form will stop
                # form being submitted
                messages.add_message(
                    request, messages.ERROR,
                    "Unfortunately," f"{customer_class_name} " "\
                        is fully booked on "
                    f"{customer_requested_date}.")

                return render(request, 'booking.html',
                              {'customer_form': customer_form,
                               'booking_form': booking_form})
            else:
                customer_email = request.POST.get('email')
                # See if customer already exists in model
                customer_query = len(Customer.objects.filter(
                    email=customer_email))

                # Prevent existing customers being dublicated to the database
                if customer_query > 0:
                    pass
                else:
                    customer_form.save()

                # Fetch customer information to pass to booking model
                current_customer = Customer.objects.get(
                    email=customer_email)
                current_customer_id = current_customer.pk
                customer = Customer.objects.get(
                    customer_id=current_customer_id)

                booking = booking_form.save(commit=False)
                # Pass formatted date & customer in to model
                booking.requested_date = date_formatted
                booking.customer = customer
                # Save booking
                booking_form.save()

                messages.add_message(
                        request, messages.SUCCESS,
                        f"Thank you {customer_name}, for booking "
                        f"{customer_class_name} on "
                        f"{customer_requested_date}! \
                            We are looking forward to sweating with you!")

                # Return blank forms so the same enquiry isn't sent twice.
                url = reverse('booking')
                return HttpResponseRedirect(url)

        else:
            messages.add_message(
                request, messages.ERROR,
                "Something went wrong with your form "
                "- please make sure your name and email address is in the"
                " correct format.")

        return render(request, 'booking.html',
                      {'customer_form': customer_form,
                       'booking_form': booking_form})


def fetch_booking(self, request, User):
    """ Get any existing bookings for the customer in the
    Booking model. If there are no bookings then redirect
    customer to Booking page.
    """
    customer_email = request.user.email
    if len(Customer.objects.filter(email=customer_email)) != 0:
        # If customer exists in model
        current_customer = Customer.objects.get(email=customer_email)
        current_customer_id = current_customer.pk

        # Get any bookings using the customer instance
        get_booking = Booking.objects.filter(
            customer=current_customer_id).values().order_by('requested_date')
            
        if len(get_booking) == 0:
            # if no bookings
            return None
        else:
            return get_booking
    else:
        # if user is not present in customer model
        return None


def validate_date(self, request, booking):
    today = datetime.datetime.now().date()
    for bookings in booking:
        if bookings['requested_date'] < today:
            bookings['status'] = 'No'

        return booking


class ManageBooking(View):
    """ View for user to manage any existing bookings """
    def get(self, request, User=User, *args, **kwargs):
        if request.user.is_authenticated:
            customer = get_customer_instance(request, User)
            current_booking = fetch_booking(self, request, User)

            # If the user has no bookings or does not exist as a 'customer'
            if current_booking is None:
                messages.add_message(
                    request, messages.WARNING,
                    "You have no session booked. No worries! "
                    "You can book here.")
                url = reverse('booking')
                return HttpResponseRedirect(url)

            else:
                validate_date(self, request, current_booking)
                return render(
                    request, 'manage_booking.html',
                    {'booking': current_booking,
                     'customer': customer})

        else:
            # Prevent users accessing this page if they are not logged in
            messages.add_message(
                request, messages.ERROR, "You must be logged in to "
                "manage your bookings.")

            url = reverse('booking')
            return HttpResponseRedirect(url)


class EditBooking(View):
    """ The view for user to be able to edit their existing bookings """
    def get(self, request, booking_id, User=User, *args, **kwargs):
        if request.user.is_authenticated:
            # Get booking object based on id
            booking = get_object_or_404(
                Booking, booking_id=booking_id)
            # Prevent customers editing outdated bookings
            today = datetime.datetime.now().date()
            if booking.requested_date < today:
                messages.add_message(
                    request, messages.ERROR, "You are trying to edit a "
                    "booking that is in the past.")
                url = reverse('manage_booking')
                return HttpResponseRedirect(url)
            # Prevent customers editing rejected bookings
            elif booking.status == 'No':
                messages.add_message(
                    request, messages.ERROR, "You are trying to edit a "
                    "booking that has been rejected.")
                url = reverse('manage_booking')
                return HttpResponseRedirect(url)
            else:
                # Convert date to display in dd/mm/YYYY format
                date_to_string = booking.requested_date.strftime(
                    "%Y-%m-%d")
                booking.requested_date = date_to_string

                # Get customer info
                customer = get_customer_instance(request, User)

                # Compare names of booking owner and user
                booking_owner = booking.customer
                name_of_user = customer

                if booking_owner != name_of_user:
                    # If the names do not match redirect to manage booking
                    messages.add_message(
                        request, messages.ERROR, "You are trying to edit a "
                        "booking that is not yours.")
                    url = reverse('manage_booking')
                    return HttpResponseRedirect(url)

                else:
                    # return both forms with the existing information
                    customer_form = CustomerForm(instance=customer)
                    booking_form = BookingForm(instance=booking)

                    return render(request, 'edit_booking.html',
                                  {'customer_form': customer_form,
                                   'customer': customer,
                                   'booking_form': booking_form,
                                   'booking': booking,
                                   'booking_id': booking_id})

        else:
            # Prevent users accessing this page if they are not logged in
            messages.add_message(
                request, messages.ERROR, "You must be logged in to "
                "manage your bookings.")

            url = reverse('booking')
            return HttpResponseRedirect(url)

    def post(self, request, booking_id, User=User, *args, **kwargs):
        customer = get_customer_instance(request, User)
        # get booking from database
        booking_id = booking_id
        booking = get_object_or_404(
            Booking, booking_id=booking_id)

        booking_form = BookingForm(
            data=request.POST, instance=booking)
        customer_form = CustomerForm(instance=customer)

        if booking_form.is_valid():
            # get the post information from the form
            customer_requested_date = request.POST.get('requested_date')
            # Convert date into format required by django
            date_formatted = datetime.datetime.strptime(
                customer_requested_date, "%Y-%m-%d").strftime('%d-%m-%Y')

            # Check the amount of bookings at that date and time
            classes_booked = check_availabilty(
                customer_requested_date, date_formatted)

            # Get the number of availble seat spot in the classes
            available_seats = classes_left()

            # Compare number of bookings to number of classes available
            if classes_booked >= Booking.seats:
                """ if the amount of classes already booked is equal to \
                the max tables then stop form from submitting. """
                messages.add_message(
                    request, messages.ERROR,
                    "Unfortunately," f"{customer_class_name} " "is fully booked on "
                    f"{customer_requested_date}.")

            else:
                # Update the existing booking with the form data.
                booking.booking_id = booking_id
                # Pass formatted date to prevent it from saving incorrectly
                booking.requested_date = date_formatted
                booking.requested_class = request.POST.get('class_name')
                # Change status to pending as the admin needs to approve
                booking.status = 'pending'
                booking_form.save(commit=False)
                booking_form.save()
                messages.add_message(request, messages.SUCCESS,
                                     f"Booking {booking_id} has now"
                                     " been updated.")
                # Fetch new list of bookings to display
                current_booking = fetch_booking(
                    self, request, User)
                validate_date(self, request, current_booking)
                # Return user to manage booking page
                return render(request, 'manage_booking.html',
                              {'booking': current_booking})

        else:
            messages.add_message(
                request, messages.ERROR,
                "Something is not right with your form "
                "- please make sure your name and email address are "
                "entered in the correct format.")

        return render(request, 'edit_booking.html',
                      {'booking_form': booking_form,
                       'customer_form': customer_form,
                       'booking': booking,
                       'customer': customer, })


class DeleteBooking(View):
    """ View for user to delete bookings """
    def get(self, request, booking_id, User=User, *args, **kwargs):
        if request.user.is_authenticated:
            booking = get_object_or_404(
                Booking, booking_id=booking_id)
            customer = get_customer_instance(request, User)
            # Prevent customers editing outdated bookings
            today = datetime.datetime.now().date()
            if booking.requested_date < today:
                messages.add_message(
                    request, messages.ERROR, "You are trying to edit a "
                    "booking that is in the past.")
                url = reverse('manage_booking')
                return HttpResponseRedirect(url)
            else:
                # Compare names of booking owner and user
                booking_owner = booking.customer
                name_of_user = customer

                if booking_owner != name_of_user:
                    # If the names do not match redirect to manage bookings
                    messages.add_message(request, messages.ERROR,
                                         "You are trying to cancel a "
                                         "booking that is not yours.")
                    url = reverse('manage_booking')
                    return HttpResponseRedirect(url)

                else:
                    return render(request, 'delete_booking.html',
                                  {'customer': customer,
                                   'booking': booking,
                                   'booking_id': booking_id})
        else:
            """Prevent users from accessing this page if not logged in""" 
            messages.add_message(
                request, messages.ERROR, "You must be logged in to "
                "manage your bookings.")

            url = reverse('booking')
            return HttpResponseRedirect(url)

    def post(self, request, booking_id, User=User, *args, **kwargs):
        # get booking from database
        booking_id = booking_id
        booking = Booking.objects.get(pk=booking_id)
        # Delete the booking
        booking.delete()
        messages.add_message(request, messages.SUCCESS,
                             f"Booking {booking_id} has now "
                             "been cancelled.")
        # Get updated list of bookings
        current_booking = fetch_booking(self, request, User)
        # Return user to manage booking page
        validate_date(self, request, current_booking)
        return render(request, 'manage_booking.html',
                      {'booking': current_booking})
