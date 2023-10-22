from rest_framework import generics, permissions
from backend.models import Area, Street, Timeslot, Appointment
from backend.serializers import AreaSerializer, StreetSerializer, TimeslotSerializer, AppointmentSerializer


class AreaList(generics.ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class AreaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class StreetList(generics.ListCreateAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer


class StreetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer


class TimeslotList(generics.ListCreateAPIView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer


class TimeslotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer


class AppointmentList(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
