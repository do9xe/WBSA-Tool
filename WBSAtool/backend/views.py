from rest_framework import generics, permissions
from backend.models import Area, Street, Timeslot, Appointment
from backend.serializers import AreaSerializer, StreetSerializer, TimeslotSerializer, AppointmentSerializer


class AreaList(generics.ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    authentication_classes = [permissions.IsAuthenticated]


class AreaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    authentication_classes = [permissions.IsAuthenticated]


class StreetList(generics.ListCreateAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
    authentication_classes = [permissions.IsAuthenticated]


class StreetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
    authentication_classes = [permissions.IsAuthenticated]


class TimeslotList(generics.ListCreateAPIView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer
    authentication_classes = [permissions.IsAuthenticated]


class TimeslotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer
    authentication_classes = [permissions.IsAuthenticated]


class AppointmentList(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    authentication_classes = [permissions.IsAuthenticated]


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    authentication_classes = [permissions.IsAuthenticated]
