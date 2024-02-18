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
        fields = ['id', 'date', 'time_from', 'time_to', 'appointment_max']


class TimeslotCountSerializer(serializers.BaseSerializer):
    class Meta:
        model = Timeslot

    def __init__(self, instance, area=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.area = area

    def to_representation(self, timeslot):
        data = {"area": AreaSerializer(self.area, read_only=True).data,
                "timeslot":TimeslotSerializer(timeslot, read_only=True).data,
                "appointment_max":timeslot.appointment_max,
                "count":timeslot.get_count_per_area(self.area),
                "percentage":timeslot.get_percentage_per_area(self.area)}
        return data


class AppointmentSerializer(serializers.ModelSerializer):
    street = StreetSerializer(read_only=True)
    timeslot = TimeslotSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'is_collected', 'area', 'contact_name', 'street', 'house_number', 'timeslot', 'text', 'phone', 'email', 'lat', 'lon']
