from django.shortcuts import render
from .models import ClassName, Session, Bookings
from django.utils.timezone import now

# Create your views here.

def session_view(request):
    """  Order the data by the date closest to the current date only for dates in the future, not for dates that have passed """

    # Show the current and upcoming dates
    today = now().date()
    classes=ClassName.objects.all()
    session_list = Session.objects.filter(session_date__gte=today).order_by('requested_date')
    
    return render(request, 'booking.html', {'classes':classes, 'session_list': session_list})


def check_availabilty(user_requested_time, user_requested_date):
    """ Check availability against Session model using customer input """

    # Check to see how many classes exist at that time/date
    classes_booked = len(Session.objects.filter(
        requested_time=user_requested_time,
        requested_date=user_requested_date, status="Available"))

    # Return number of classes
    return classes_booked

# today = datetime.now().strftime('%Y-%m-%d')
# Session_data = Session.objects.filter(active='a').filter((date__gte=today)|(date=today)).order_by('date')

  