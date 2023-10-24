from rest_framework import serializers
from backend.models import Area, Street, Timeslot, Appointment


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name', 'is_parent', 'parent']


class StreetSerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True)

    class Meta:
        model = Street
        fields = ['id', 'name', 'area', 'osm_imported']


class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        fields = ['id', 'date', 'time_from', 'time_to', 'appointment_max', 'appointment_count', 'is_full']


class AppointmentSerializer(serializers.ModelSerializer):
    street = StreetSerializer(read_only=True)
    timeslot = TimeslotSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'is_collected', 'contact_name', 'street', 'house_number', 'timeslot', 'text', 'phone', 'email', 'lat', 'lon']
