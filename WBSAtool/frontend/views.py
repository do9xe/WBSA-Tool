from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
import requests

from .models import Area, Street, Timeslot, Appointment


@permission_required("frontend.view_area", raise_exception=True)
def area_list(request):
    if request.method == 'GET':
        AreaList = Area.objects.all()
        context = {'area_list': AreaList}
        return render(request, 'area/area_list.html', context)


@permission_required("frontend.delete_area", raise_exception=True)
def area_delete(request):
    if request.method == 'POST':
        if request.POST['action'] == "delete_areas":
            for id in request.POST.getlist('select_row'):
                Area.objects.get(id=int(id)).delete()
            return HttpResponseRedirect(reverse('wbsa:area_list'))
        elif request.POST['action']:
            id = int(request.POST['action'])
            Area.objects.get(id=id).delete()
            return HttpResponseRedirect(reverse('wbsa:area_list'))


@permission_required("frontend.view_area", raise_exception=True)
def area_view(request, area_id):
    if request.GET['format'] == "modal":
        area = get_object_or_404(Area, id=area_id)
        if area.is_parent:
            AreaList = Area.objects.filter(parent=area)
            StreetList = []
            for subarea in AreaList:
                l = Street.objects.filter(area=subarea)
                for street in l:
                    StreetList.append(street)
        else:
            StreetList = Street.objects.filter(area=area)
        context = {'area': area, 'street_list': StreetList}
        return render(request, 'area/area_modal.html', context)
    else:
        return HttpResponse("Error, only intended von indirect use")


@permission_required("frontend.change_area", raise_exception=True)
def area_edit(request, area_id):
    area = get_object_or_404(Area, id=area_id)
    if request.method == 'GET':
        AreaList = Area.objects.filter(is_parent=True)
        context = {'area': area, 'parent_area_list': AreaList}
        return render(request, 'area/area_edit.html', context)
    if request.method == 'POST':
        area.name = request.POST['name']
        if 'is_parent' in request.POST:
            area.is_parent = True
        else:
            area.is_parent = False
        if request.POST['parent'] != "None":
            selected_parent = get_object_or_404(Area, id=request.POST['parent'])
            area.parent = selected_parent
        else:
            area.parent = None
        area.save()
        return HttpResponseRedirect(reverse('wbsa:area_list'))


@permission_required("frontend.add_area", raise_exception=True)
def area_new(request):
    if request.method == 'GET':
        AreaList = Area.objects.filter(is_parent=True)
        context = {'parent_area_list': AreaList}
        return render(request, 'area/area_edit.html', context)
    if request.method == 'POST':
        newArea = Area(name=request.POST['name'])
        if 'is_parent' in request.POST:
            newArea.is_parent = True
        if request.POST['parent'] != "None":
            selected_parent = get_object_or_404(Area, id=request.POST['parent'])
            newArea.parent = selected_parent
        newArea.save()
        return HttpResponseRedirect(reverse('wbsa:area_list'))


@permission_required("frontend.view_street", raise_exception=True)
def street_list(request):
    if request.method == 'GET':
        StreetList = Street.objects.all()
        context = {'street_list': StreetList}
        return render(request, 'street/street_list.html', context)


@permission_required("frontend.delete_street", raise_exception=True)
def street_delete(request):
    if request.method == 'POST':
        if request.POST['action'] == "delete":
            for id in request.POST.getlist('select_row'):
                Street.objects.get(id=int(id)).delete()
            return HttpResponseRedirect(reverse('wbsa:street_list'))


@permission_required("frontend.change_street", raise_exception=True)
def street_edit(request, street_id):
    street = get_object_or_404(Street, id=street_id)
    if request.method == 'GET':
        AreaList = Area.objects.filter(is_parent=False)
        context = {'street': street, 'area_list': AreaList}
        return render(request, 'street/street_edit.html', context)
    if request.method == 'POST':
        street.name = request.POST['name']
        if request.POST['area'] != "None":
            selected_parent = get_object_or_404(Area, id=request.POST['area'])
            street.area = selected_parent
        else:
            street.area = None
        street.save()
        return HttpResponseRedirect(reverse('wbsa:street_list'))


@permission_required("frontend.add_street", raise_exception=True)
def street_bulkadd(request):
    if request.method == 'GET':
        return render(request, 'street/street_bulk_add.html')
    if request.method == 'POST':
        ImportList = request.POST['data'].split("\r\n")
        header_raw = ImportList.pop(0)
        header = header_raw.split(",")
        if (header[0] == "street") and (header[1] == "area"):
            for line in ImportList:
                street = line.split(",")[0]
                newStreet = Street(name=street)
                if len(line.split(",")) > 1:
                    try:
                        area_name = line.split(",")[1]
                        AreaObject = Area.objects.get(name=area_name)
                        newStreet.area = AreaObject
                    except Area.DoesNotExist as e:
                        pass
                newStreet.save()
            return HttpResponseRedirect(reverse('wbsa:street_list'))
        else:
            error_message = f"Falscher CSV-Header: {header_raw}"
            context = {"error_message": error_message}
            return render(request, "error_page.html", context)


@permission_required("frontend.view_timeslot", raise_exception=True)
def timeslot_list(request):
    if request.method == "GET":
        TimeslotList = Timeslot.objects.all()
        context = {'timeslot_list': TimeslotList}
        return render(request, 'timeslot/timeslot_list.html', context)


@permission_required("frontend.delete_timeslot", raise_exception=True)
def timeslot_delete(request):
    if request.method == 'POST':
        if request.POST['action'] == "delete":
            for id in request.POST.getlist('select_row'):
                Timeslot.objects.get(id=int(id)).delete()
            return HttpResponseRedirect(reverse('wbsa:timeslot_list'))


@permission_required("frontend.add_timeslot", raise_exception=True)
def timeslot_new(request):
    if request.method == "GET":
        return render(request, "timeslot/timeslot_edit.html")
    elif request.method == "POST":
        timeslot = Timeslot()
        timeslot.date = request.POST['date']
        timeslot.time_from = request.POST['time_from']
        timeslot.time_to = request.POST['time_to']
        timeslot.save()
        return HttpResponseRedirect(reverse('wbsa:timeslot_list'))


@permission_required("frontend.change_timeslot", raise_exception=True)
def timeslot_edit(request, timeslot_id):
    timeslot = get_object_or_404(Timeslot, id=timeslot_id)
    if request.method == "GET":
        context = {"timeslot": timeslot}
        return render(request, "timeslot/timeslot_edit.html", context)
    elif request.method == "POST":
        timeslot.date = request.POST['date']
        timeslot.time_from = request.POST['time_from']
        timeslot.time_to = request.POST['time_to']
        timeslot.save()
        return HttpResponseRedirect(reverse('wbsa:timeslot_list'))


@permission_required("frontend.add_appointment", raise_exception=True)
def timeslot_suggestion(request):
    street = get_object_or_404(Street, name=request.GET['street'])
    TimeslotList = Timeslot.objects.all()
    SuggestionList = []
    for Slot in TimeslotList:
        count = Appointment.objects.filter(timeslot=Slot, street=street).count()
        if count != 0:
            suggestion = {"timeslot": Slot, "count": count}
            SuggestionList.append(suggestion)
    if len(SuggestionList) == 0:
        return HttpResponse("")
    context = {"suggestion_list": SuggestionList}
    return render(request, "timeslot/timeslot_suggestion.html", context)


@permission_required("frontend.view_appointment", raise_exception=True)
def appointment_list(request):
    if request.method == "GET":
        AppointmentList = Appointment.objects.all()
        context = {'appointment_list': AppointmentList}
        return render(request, 'appointment/appointment_list.html', context)


@permission_required("frontend.delete_appointment", raise_exception=True)
def appointment_delete(request):
    if request.method == "POST":
        if request.POST['action'] == "delete":
            for id in request.POST.getlist('select_row'):
                Appointment.objects.get(id=int(id)).delete()
            return HttpResponseRedirect(reverse('wbsa:appointment_list'))


@permission_required("frontend.view_appointment", raise_exception=True)
def appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.GET['format'] == "modal":
        context = {'appointment': appointment}
        return render(request, 'appointment/appointment_modal.html', context)


@permission_required("frontend.change_appointment", raise_exception=True)
def appointment_edit(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'GET':
        StreetList = Street.objects.all()
        TimeslotList = Timeslot.objects.all()
        context = {"appointment": appointment, "street_list": StreetList, 'timeslot_list': TimeslotList}
        return render(request, 'appointment/appointment_edit.html', context)
    if request.method == "POST":
        appointment.contact_name = request.POST['name']
        appointment.street = get_object_or_404(Street, name=request.POST['street'])
        appointment.house_number = request.POST['house_number']
        appointment.timeslot = get_object_or_404(Timeslot, id=request.POST['timeslot'])
        appointment.text = request.POST['text']
        appointment.phone = request.POST['phone']
        appointment.email = request.POST['email']
        appointment.save()
        return HttpResponseRedirect(reverse('wbsa:appointment_list'))


@permission_required("frontend.add_appointment", raise_exception=True)
def appointment_new(request):
    if request.method == 'GET':
        StreetList = Street.objects.all()
        TimeslotList = Timeslot.objects.all()
        context = {"street_list": StreetList, 'timeslot_list': TimeslotList}
        return render(request, 'appointment/appointment_edit.html', context)
    if request.method == "POST":
        contact_name = request.POST['name']
        street = get_object_or_404(Street, name=request.POST['street'])
        house_number = request.POST['house_number']
        timeslot = get_object_or_404(Timeslot, id=request.POST['timeslot'])
        text = request.POST['text']
        phone = request.POST['phone']
        email = request.POST['email']
        newAppointment = Appointment(contact_name=contact_name, street=street, house_number=house_number, timeslot=timeslot)
        if text:
            newAppointment.text = text
        if phone:
            newAppointment.phone = phone
        if email:
            newAppointment.email = email
        newAppointment.save()
        return HttpResponseRedirect(reverse('wbsa:appointment_map'))


@login_required(login_url='/auth/login')
def appointment_map(request):
    AppointmentList = Appointment.objects.all()
    context = {'appointment_list': AppointmentList}
    return render(request, 'appointment/map.html', context)


@permission_required("frontend.add_street", raise_exception=True)
def street_osm_import(request):
    if request.method == "GET":
        plz = request.GET['plz']
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f'''
        [out:json][timeout:25];
        area[postal_code="{plz}"];
        way(area)[highway~"^(residential|living_street|secondary|tertiary)$"];
        out;
        '''
        response = requests.get(overpass_url, params={'data': overpass_query})
        raw_data = response.json()
        street_list = []
        for street in raw_data['elements']:
            if "name" in street['tags']:
                street_list.append(street['tags']['name'])
        street_list = list(dict.fromkeys(street_list))
        for street in street_list:
            new_street = Street(name=street)
            new_street.osm_imported = True
            new_street.save()
        return HttpResponse(str(street_list))
