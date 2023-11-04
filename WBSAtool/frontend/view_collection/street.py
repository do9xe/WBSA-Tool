from .generic import WBSAListView, WBSACreateView, WBSAUpdateView, WBSABulkUpdateView
from backend.models import Street
from frontend.forms import StreetForm, BulkUpdateStreetForm


class StreetListView(WBSAListView):
    model = Street
    context_object_name = "street_list"
    template_name = "street/street_list.html"


class StreetCreateView(WBSACreateView):
    model = Street
    form_class = StreetForm
    redirect_to = "frontend:street_list"


class StreetUpdateView(WBSAUpdateView):
    model = Street
    form_class = StreetForm
    redirect_to = "frontend:street_list"


class StreetBulkUpdateView(WBSABulkUpdateView):
    model = Street
    form_class = BulkUpdateStreetForm
    template_name = "bulk_edit.html"
    redirect_to = "frontend:street_list"
