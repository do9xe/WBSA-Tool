from django.contrib import admin

from .models import Area, Street, Timeslot, Appointment

admin.site.register(Area)
admin.site.register(Street)
admin.site.register(Timeslot)
admin.site.register(Appointment)
