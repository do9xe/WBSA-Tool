from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .generic import WBSAListView
from backend.models import Appointment


class AppointmentListView(WBSAListView):
    model = Appointment
    context_object_name = "appointment_list"
    template_name = "appointment/appointment_list.html"


class UpdateAppointmentCollected(UpdateView):
    model = Appointment
    fields = ['is_collected']
    pk_url_kwarg = "appointment_id"
    success_url = "/mobile/menu"


class AppointmentMapView(LoginRequiredMixin, TemplateView):
    template_name = "appointment/map.html"
