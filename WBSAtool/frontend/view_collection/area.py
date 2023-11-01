from .generic import WBSAListView, WBSAUpdateView, WBSACreateView
from frontend.forms import AreaForm
from backend.models import Area


class AreaListView(WBSAListView):
    model = Area
    context_object_name = "area_list"
    template_name = "area/area_list.html"


class AreaCreateView(WBSACreateView):
    model = Area
    form_class = AreaForm
    template_name = "area/area_edit.html"
    redirect_to = "frontend:area_list"


class AreaUpdateView(WBSAUpdateView):
    model = Area
    form_class = AreaForm
    template_name = "area/area_edit.html"
    redirect_to = "frontend:area_list"
