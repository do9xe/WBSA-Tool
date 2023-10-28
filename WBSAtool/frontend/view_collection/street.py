from .generic import WBSAListView, WBSACreateView, WBSAUpdateView
from backend.models import Street
from frontend.forms import StreetForm


class StreetListView(WBSAListView):
    model = Street
    context_object_name = "street_list"
    template_name = "street/street_list.html"


class NewStreetView(WBSACreateView):
    model = Street
    form_class = StreetForm
    template_name = "street/street_edit.html"
    redirect_to = "frontend:street_list"


class UpdateStreetView(WBSAUpdateView):
    model = Street
    form_class = StreetForm
    template_name = "street/street_edit.html"
    redirect_to = "frontend:street_list"
