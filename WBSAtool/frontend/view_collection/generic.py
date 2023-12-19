from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect, render
from django.urls import reverse
from backend.models import Street


class WBSAPermissionMixin(PermissionRequiredMixin):
    required_list = []

    def get_permission_required(self):
        for code in self.required_list:
            codename = f"backend.{code}_{self.model._meta.model_name}"
            print(codename)
            yield codename


class WBSAListView(WBSAPermissionMixin, ListView):
    required_list = ["view"]


class WBSACreateView(WBSAPermissionMixin, CreateView):
    required_list = ["add"]
    redirect_to = ""
    template_name = "model_edit.html"

    def get_success_url(self):
        return reverse(self.redirect_to)


class WBSAUpdateView(WBSAPermissionMixin, UpdateView):
    required_list = ["change"]
    redirect_to = ""
    template_name = "model_edit.html"

    def get_success_url(self):
        return reverse(self.redirect_to)


class WBSABulkUpdateView(WBSAPermissionMixin, View):
    model = None
    form_class = None
    required_list = ["change"]
    redirect_to = ""
    template_name = ""

    def update_objects(self, form):
        for obj in self.model.objects.filter(id__in=form.cleaned_data["select_row"]):
            for field in form.changed_data:
                if field in [f.name for f in self.model._meta.fields]:
                    setattr(obj, field, form.cleaned_data[field])
                    obj.full_clean()
                    obj.save()

    def get(self, request):
        return redirect(reverse(self.redirect_to))

    def post(self, request):
        if request.POST.get("select_all"):
            id_list = self.model.objects.all().values_list("id", flat=True)
        else:
            id_list = request.POST.getlist("select_row")
        if len(id_list) == 0:
            return redirect(reverse(self.redirect_to))

        initial_data = {"id_list": id_list}

        if "_save" in request.POST:
            form = self.form_class(request.POST, initial=initial_data)

            if form.is_valid():
                self.update_objects(form)
                return redirect(reverse(self.redirect_to))
        else:
            form = self.form_class(initial=initial_data)

        return render(request, self.template_name, {
            "model": self.model,
            "form": form,
            "redirect_to": self.redirect_to
        })