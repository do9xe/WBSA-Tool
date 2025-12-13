import json

from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from .generic import WBSAListView
from backend.models import Appointment, Area, Timeslot


class AppointmentListView(WBSAListView):
    model = Appointment
    ordering = ["timeslot__date", "timeslot__time_from"]
    context_object_name = "appointment_list"
    template_name = "appointment/appointment_list.html"


class AppointmentDispoView(WBSAListView):
    model = Appointment
    ordering = ["street"]
    context_object_name = "appointment_list"
    template_name = "appointment/appointment_dispo.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AppointmentDispoView, self).get_context_data(**kwargs)
        context.update({
            'area_list': Area.objects.filter(is_parent=True).order_by("name"),
            'timeslot_list': Timeslot.objects.order_by("date", "time_from"),
        })
        return context

    def post(self, request, *args, **kwargs):
        data = json.loads(request.POST.get("data"))
        for areaStr in data:
            areaId = int(areaStr.split("_")[1])
            areaObj = Area.objects.get(id=areaId)
            for appointmentStr in data[areaStr]:
                appointmentId = int(appointmentStr.split("_")[1])
                appointmentObj = Appointment.objects.get(id=appointmentId)
                if appointmentObj.street.area.parent == areaObj:
                    appointmentObj.area = None
                else:
                    appointmentObj.area = areaObj
                appointmentObj.save()
        return HttpResponseRedirect(reverse("frontend:appointment_list"))


class UpdateAppointmentCollected(UpdateView):
    model = Appointment
    fields = ['is_collected']
    pk_url_kwarg = "appointment_id"
    success_url = "/mobile/menu"


class AppointmentMapView(LoginRequiredMixin, TemplateView):
    template_name = "appointment/map.html"


class AppointmentStatsView(LoginRequiredMixin, TemplateView):
    template_name = "appointment/stats.html"
