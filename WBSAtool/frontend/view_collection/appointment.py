from .generic import WBSAListView
from ..models import Appointment


class AppointmentListView(WBSAListView):
    model = Appointment
    context_object_name = "appointment_list"
    template_name = "appointment/appointment_list.html"
