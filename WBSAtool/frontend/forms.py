from django import forms
from backend.models import Area, Street, Timeslot
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


class StreetForm(forms.ModelForm):
    class Meta:
        model = Street
        exclude = ["osm_imported"]
    name = forms.CharField(label="Straßenname",
                           max_length=200,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    area = forms.ModelChoiceField(label="Gebiet",
                                  queryset=Area.objects.filter(is_parent=False),
                                  widget=forms.Select(attrs={'class': 'form-select'}))


class BulkUpdateStreetForm(forms.Form):
    area = forms.ModelChoiceField(label="Gebiet",
                                  queryset=Area.objects.filter(is_parent=False),
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    select_row = forms.ModelMultipleChoiceField(queryset=Street.objects.all(),
                                                widget=forms.MultipleHiddenInput,
                                                )
