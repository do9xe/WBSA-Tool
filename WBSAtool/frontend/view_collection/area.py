from .generic import WBSAListView
from backend.models import Area


class AreaListView(WBSAListView):
    model = Area
    context_object_name = "area_list"
    template_name = "area/area_list.html"
