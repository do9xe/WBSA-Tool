from django.shortcuts import get_object_or_404
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.models import Area, Street, Timeslot, Appointment
from backend.serializers import AreaSerializer, StreetSerializer, TimeslotSerializer, TimeslotCountSerializer, AppointmentSerializer


class AreaList(generics.ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    filterset_fields = ['id', 'name', 'is_parent']


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
    filterset_fields = ['id', 'date', 'time_from', 'time_to', 'appointment_max']


class TimeslotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer


class TimeslotCount(APIView):
    def get(self, request, pk):
        area = get_object_or_404(Area, id=pk)
        timeslot = Timeslot.objects.order_by("date", "time_from")
        data = TimeslotCountSerializer(timeslot, area=area, many=True).data
        return Response(data=data)


class singleTimeslotCount(APIView):
    def get(self, request, pk):
        if "area" in request.GET:
            area = get_object_or_404(Area, id=request.GET['area'])
            timeslot = get_object_or_404(Timeslot, id=pk)
            data = TimeslotCountSerializer(timeslot, area=area).data
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AppointmentList(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filterset_fields = ['id', 'is_collected', 'contact_name', 'street', 'house_number', 'timeslot', 'text', 'phone', 'email']


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
