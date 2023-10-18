from .generic import WBSAListView
from backend.models import Timeslot


class TimeslotListView(WBSAListView):
    model = Timeslot
    context_object_name = "timeslot_list"
    template_name = "timeslot/timeslot_list.html"