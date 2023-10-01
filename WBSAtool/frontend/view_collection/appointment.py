from django.views.generic.edit import UpdateView
from .generic import WBSAListView
from ..models import Appointment


class AppointmentListView(WBSAListView):
    model = Appointment
    context_object_name = "appointment_list"
    template_name = "appointment/appointment_list.html"


class UpdateAppointmentCollected(UpdateView):
    model = Appointment
    fields = ['is_collected']
    pk_url_kwarg = "appointment_id"
    success_url = "/mobile/menu"