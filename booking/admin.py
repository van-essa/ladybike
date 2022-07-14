from django.contrib import admin
from .models import Session, ClassName, Bookings

# Register your models here.
@admin.register(ClassName)
class ClassNameAdmin(admin.ModelAdmin):
    list_display = ('classes',)


@admin.register(Session)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('class_name','status', 'requested_date', 'requested_time')
    search_fields = ['class_name']
    list_filter = ('status',)

@admin.register(Bookings)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('session', 'sessiondate', 'bookingstatus',)


    