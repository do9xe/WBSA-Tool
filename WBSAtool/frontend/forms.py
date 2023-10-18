from django import forms
from backend.models import Area, Timeslot
from django.forms.models import ModelChoiceField


class TimeslotChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.date}, {obj.time_from} bis {obj.time_to}"


class CollectMenuForm(forms.Form):
    area = forms.ModelChoiceField(queryset=Area.objects.filter(is_parent=True),
                                  label="Fahrzeug",
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    timeslot = TimeslotChoiceField(queryset=Timeslot.objects.all(),
                                   label="Zeitraum",
                                   widget=forms.Select(attrs={'class': 'form-select'}))

