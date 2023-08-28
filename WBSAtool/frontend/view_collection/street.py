from .generic import WBSAListView
from ..models import Street


class StreetListView(WBSAListView):
    model = Street
    context_object_name = "street_list"
    template_name = "street/street_list.html"