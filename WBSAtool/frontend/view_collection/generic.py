from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView


class WBSAListView(PermissionRequiredMixin, ListView):
    def get_permission_required(self):
        required_list = ["view"]
        for code in required_list:
            codename = f"frontend.{code}_{self.model._meta.model_name}"
            yield codename
