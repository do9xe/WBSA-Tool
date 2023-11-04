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
        titel = "Straße bearbeiten"
    name = forms.CharField(label="Straßenname",
                           max_length=200,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    area = forms.ModelChoiceField(label="Gebiet",
                                  queryset=Area.objects.filter(is_parent=False),
                                  widget=forms.Select(attrs={'class': 'form-select'}))


class BulkUpdateStreetForm(forms.Form):
    class Meta:
        titel = "mehrere Straßen bearbeiten"
    area = forms.ModelChoiceField(label="Gebiet",
                                  queryset=Area.objects.filter(is_parent=False),
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    select_row = forms.ModelMultipleChoiceField(queryset=Street.objects.all(),
                                                widget=forms.MultipleHiddenInput)


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        exclude = []
        titel = "Gebiet bearbeiten"
    name = forms.CharField(label="Name",
                           max_length=200,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_parent = forms.BooleanField(label="Ist ein Fahrzeug",
                                   required=False,
                                   widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    parent = forms.ModelChoiceField(label="Fahrzeug",
                                    required=False,
                                    queryset=Area.objects.filter(is_parent=True),
                                    widget=forms.Select(attrs={'class': 'form-select'}))
