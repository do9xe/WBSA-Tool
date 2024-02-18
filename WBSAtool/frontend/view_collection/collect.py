from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.urls import reverse
from django.utils.html import urlencode
from itertools import chain
from ..forms import CollectMenuForm
from backend.models import Appointment


class CollectMenu(FormView):
    template_name = "collect/collect_menu.html"
    form_class = CollectMenuForm
    success_url = ""

    def form_valid(self, form):
        url = reverse("frontend:collect_list")
        parameters = urlencode({"area": form.cleaned_data['area'].id, "timeslot": form.cleaned_data['timeslot'].id})
        self.success_url = f"{url}?{parameters}"
        return super().form_valid(form)


class CollectList(ListView):
    template_name = "collect/collect_list.html"
    model = Appointment

    def get_queryset(self):
        qs = self.model.objects.all()
        if "area" in self.request.GET:
            area = int(self.request.GET['area'])
            overwrites = self.model.objects.filter(area_id=area)
            qs = qs.filter(street__area__parent_id=area, area__isnull=True) | overwrites
        if "timeslot" in self.request.GET:
            timeslot = int(self.request.GET['timeslot'])
            qs = qs.filter(timeslot_id=timeslot)
        return qs


