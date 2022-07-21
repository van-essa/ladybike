from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class ClassName(models.Model):
    """ Class Type Model """
    
    CLASS_CHOICES = ((1, 'Spinning'),
                     (2, 'Ride_that_hill'),
                     (3, 'LadyBike'))

    classes = models.IntegerField(choices=CLASS_CHOICES, primary_key=True)

    def __str__(self):
        return str(self.classes)

class Session(models.Model):
    """ Session Class Model """

    STATUS_CHOICES = (('Fully_Booked', 'Fully_Booked'),
                      ('Availble', 'Availble'))

    class Meta:
        verbose_name_plural = 'Sessions'

    class_name = models.ForeignKey('ClassName', on_delete=models.CASCADE, default=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Available')
    seats = models.IntegerField(default=True, null=False)
    requested_date = models.DateField()
    requested_time = models.TimeField()

    def __str__(self):
        return str(self.class_name)


    @property
    """ Counting the amount of classes available that got booked """
    def classes_total(self):
        return self.class_name.filter(classstatus='Available').count()
    
    @property
    """ Removing the booked seats with the total availbel seats """
    def classes_left(self):
        return self.classes_total - self.seats
    


class Bookings(models.Model):
    """ Booking Model """

    OPTION_STATUS = (('y','Yes'), ('n', 'No'), ('p', 'Pending'))

    booking_id = models.AutoField(primary_key=True)
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    sessiondate = models.DateField()
    bookingstatus = models.CharField(max_length=10, default='p', choices=OPTION_STATUS)
    
    def __str__(self):
        return str(self.booking_id)
