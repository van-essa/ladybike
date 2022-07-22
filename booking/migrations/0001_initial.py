# Generated by Django 3.2.14 on 2022-07-22 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassName',
            fields=[
                ('classes', models.IntegerField(choices=[(1, 'Spinning'), (2, 'Ride_that_hill'), (3, 'LadyBike')], primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(default='', max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('Fully_Booked', 'Fully_Booked'), ('Availble', 'Availble')], default='Available', max_length=15)),
                ('seats', models.IntegerField(default=True)),
                ('requested_date', models.DateField()),
                ('requested_time', models.TimeField()),
                ('bookingtatus', models.CharField(choices=[('y', 'Yes'), ('n', 'No'), ('p', 'Pending')], default='p', max_length=10)),
                ('class_name', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='booking.classname')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='booking.customer')),
            ],
            options={
                'verbose_name_plural': 'Booking',
            },
        ),
    ]
