from django.contrib import admin
from .models import ClassName, Customer, Booking

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'full_name', 'email',)


@admin.register(ClassName)
class ClassNameAdmin(admin.ModelAdmin):
    list_display = ('classes',)
    

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    search_fields = ['class_name']
    list_filter = ('class_name', 'status')
    list_display = ('booking_id', 'class_name', 'customer', 'status',
                    'requested_date', 'requested_time',)


    


    