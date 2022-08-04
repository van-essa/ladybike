from django.db import models


# Create your models here.
class Customer(models.Model):
    """ Customer information model """
    customer_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, default="")

    def __str__(self):
        # return the full name as this is easier for the admin to read
        return self.full_name


class ClassName(models.Model):
    """ Class Type Model """

    CLASS_CHOICES = ((1, 'Spinning'),
                     (2, 'Ride_that_hill'),
                     (3, 'LadyBike'))

    classes = models.IntegerField(choices=CLASS_CHOICES, primary_key=True)

    def __str__(self):
        return str(self.classes)


class Booking(models.Model):
    """ Booking Class Model """

    STATUS_CHOICES = (('Fully_Booked', 'Fully_Booked'),
                      ('Availble', 'Availble'))

    OPTION_STATUS = (('y', 'Yes'), ('n', 'No'), ('p', 'Pending'))

    class Meta:
        """Booking Meta"""
        verbose_name_plural = 'Booking'

    booking_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer", null=True)
    class_name = models.ForeignKey(
        'ClassName', on_delete=models.CASCADE, default=True)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='Available')
    seats = models.IntegerField(default=True, null=False)
    requested_date = models.DateField()
    bookingtatus = models.CharField(
        max_length=10, default='p', choices=OPTION_STATUS)

    def __str__(self):
        return str(self.class_name)


@property
def classes_total(self):
    """ Counting the amount of classes available that got booked """
    return self.class_name.filter(classstatus='Available').count()


@property
def classes_left(self):
    """ Removing the booked seats with the total availbel seats """
    return self.classes_total - self.seats
