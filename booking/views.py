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

def booking_view(request):
    """  Order the data by the date closest to the current date only for dates in the future, not for dates that have passed """

    # Show the current and upcoming dates
    today = now().date()
    classes=ClassName.objects.all()
    booking_list = Booking.objects.filter(booking_date__gte=today).order_by('requested_date')
    
    return render(request, 'booking.html', {'classes':classes, 'booking_list': booking_list})

def get_customer_instance(request, User):
    """ Returns customer instance if User is logged in """
    customer_email = request.user.email
    customer = Customer.objects.filter(email=customer_email).first()

    return customer

""" Counting the amount of classes available that got booked """
    def classes_total():
        return Booking.class_name.filter(classstatus='Available').count()
    

    """ Removing the booked seats with the total available seats """
    def classes_left():
        return Booking.classes_total - Booking.seats


def check_availabilty(user_requested_time, user_requested_date):
    """ Check availability against Booking model using customer input """

    # Check to see how many classes exist at that time/date
    classes_booked = len(Booking.objects.filter(
        class_name=customer_class_name,
        requested_time=customer_requested_time,
        requested_date=customer_requested_date, status="Available"))

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
                      {'customer_form': customer_form,
                       'booking_form': booking_form})
    

    def post(self, request, User=User, *args, **kwargs):
        # Get post data from forms
        customer_form = CustomerForm(data=request.POST)
        booking_form = BookingForm(data=request.POST)

        if customer_form.is_valid() and reservation_form.is_valid():
            # Fetch information from forms
            customer_class_name = requesr.POST.get('class_name')
            customer_requested_date = request.POST.get('requested_date')
            customer_requested_time = request.POST.get('requested_time')
            customer_name = request.POST.get('full_name')

            # Convert date in to format required by django
            date_formatted = datetime.datetime.strptime(
                customer_requested_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            
            # Check to see how many bookings exist at that time/date
            classes_booked = check_availabilty(
                customer_requested_time, date_formatted)

            # Get the number of availble seat spot in the classes
            available_seats = classes_left()

            # Compare number of bookings to number of classes available
            if classes_booked >= classes_left:
                """ If the number of classes booked is bigger than or equal to the
                max number of classes left in the LadyBike Gym, the form will stop 
                form being submitted
                """
                messages.add_message(
                    request, messages.ERROR,
                    "Unfortunately," f"{customer_class_name} " "is fully booked at "
                    f"{customer_requested_time} on {customer_requested_date}.")

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
                        f"{customer_class_name} at "
                        f"{customer_requested_time} on "
                        f"{customer_requested_date}! We are looking forward to sweating with you!")

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
        if bookongs['requested_date'] < today:
            bookings['status'] = 'expired'

        return booking
        

# today = datetime.now().strftime('%Y-%m-%d')
# Booking_data = Booking.objects.filter(active='a').filter((date__gte=today)|(date=today)).order_by('date')

  