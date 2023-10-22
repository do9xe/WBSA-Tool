from rest_framework import generics

from backend.models import Area, Street, Timeslot, Appointment
from backend.serializers import AreaSerializer, StreetSerializer, TimeslotSerializer, AppointmentSerializer


class AreaList(generics.ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    filterset_fields = ['id', 'name', 'ist_parent']


class AreaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class StreetList(generics.ListCreateAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
    filterset_fields = ['id', 'name', 'area', 'osm_imported']


class StreetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer


class TimeslotList(generics.ListCreateAPIView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer
    filterset_fields = ['id', 'date', 'time_from', 'time_to', 'appointment_max', 'appointment_count', 'is_full']


class TimeslotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer


class AppointmentList(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filterset_fields = ['id', 'is_collected', 'contact_name', 'street', 'house_number', 'timeslot', 'text', 'phone', 'email']


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
