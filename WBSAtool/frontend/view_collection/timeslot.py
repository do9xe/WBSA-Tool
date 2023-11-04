from .generic import WBSAListView, WBSACreateView, WBSAUpdateView
from frontend.forms import TimeslotForm
from backend.models import Timeslot


class TimeslotListView(WBSAListView):
    model = Timeslot
    context_object_name = "timeslot_list"
    template_name = "timeslot/timeslot_list.html"


class TimeslotCreateView(WBSACreateView):
    model = Timeslot
    form_class = TimeslotForm
    redirect_to = "frontend:timeslot_list"


class TimeslotUpdateView(WBSAUpdateView):
    model = Timeslot
    form_class = TimeslotForm
    redirect_to = "frontend:timeslot_list"
