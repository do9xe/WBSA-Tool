from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse


class WBSAPermissionMixin(PermissionRequiredMixin):
    def get_permission_required(self):
        for code in self.required_list:
            codename = f"backend.{code}_{self.model._meta.model_name}"
            yield codename


class WBSAListView(WBSAPermissionMixin, ListView):
    required_list = ["view"]


class WBSACreateView(WBSAPermissionMixin, CreateView):
    required_list = ["create"]
    redirect_to = "/"

    def get_success_url(self):
        return reverse(self.redirect_to)


class WBSAUpdateView(WBSAPermissionMixin, UpdateView):
    required_list = ["create"]
    redirect_to = "/"

    def get_success_url(self):
        return reverse(self.redirect_to)
