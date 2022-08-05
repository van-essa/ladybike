"""Imports"""
from django.shortcuts import render, redirect
from booking.models import Customer


# Create your views here.
def index(request):
    """ Return homepage """
    return render(request, 'index.html')


def sign_up(request):
    """Sign Up"""
    if request.method == "POST":
        form = Customer(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = Customer() 
    return render(request, 'signup.html', {'form': form})


def get_customer_instance(request, User):
    """ Returns customer instance if User is logged in """
    customer_email = request.user.email
    customer = Customer.objects.filter(email=customer_email).first()

    return customer


def error_403(request, exception):
    """ 403 error page """
    return render(request, '403.html', status=403)


def error_404(request, exception):
    """ 404 error page """
    return render(request, '404.html', status=404)


def error_500(request):
    """ 500 error page """
    return render(request, '500.html', status=500)
