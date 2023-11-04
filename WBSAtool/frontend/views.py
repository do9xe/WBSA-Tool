from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
import requests

from backend.models import Area, Street, Timeslot, Appointment
from .utils.ReportLabWrapper import ReportLab, wrap_text


@permission_required("frontend.delete_area", raise_exception=True)
def area_delete(request):
    if request.method == 'POST':
        if request.POST['action'] == "delete_areas":
            for id in request.POST.getlist('select_row'):
                Area.objects.get(id=int(id)).delete()
            return HttpResponseRedirect(reverse('frontend:area_list'))
        elif request.POST['action']:
            id = int(request.POST['action'])
            Area.objects.get(id=id).delete()
            return HttpResponseRedirect(reverse('frontend:area_list'))


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


@permission_required("frontend.delete_street", raise_exception=True)
def street_delete(request):
    if request.method == 'POST':
        if request.POST['action'] == "delete":
            for id in request.POST.getlist('select_row'):
                Street.objects.get(id=int(id)).delete()
            return HttpResponseRedirect(reverse('frontend:street_list'))


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
            return HttpResponseRedirect(reverse('frontend:street_list'))
        else:
            error_message = f"Falscher CSV-Header: {header_raw}"
            context = {"error_message": error_message}
            return render(request, "error_page.html", context)


@permission_required("frontend.delete_timeslot", raise_exception=True)
def timeslot_delete(request):
    if request.method == 'POST':
        if request.POST['action'] == "delete":
            for id in request.POST.getlist('select_row'):
                Timeslot.objects.get(id=int(id)).delete()
            return HttpResponseRedirect(reverse('frontend:timeslot_list'))


@permission_required("frontend.add_appointment", raise_exception=True)
def timeslot_suggestion(request):
    street = get_object_or_404(Street, name=request.GET['street'])
    TimeslotList = Timeslot.objects.all()
    SuggestionList = []
    for Slot in TimeslotList:
        if Slot.is_full:
            continue
        count = Appointment.objects.filter(timeslot=Slot, street=street).count()
        if count != 0:
            suggestion = {"timeslot": Slot, "count": count}
            SuggestionList.append(suggestion)
    if len(SuggestionList) == 0:
        return HttpResponse("")
    context = {"suggestion_list": SuggestionList}
    return render(request, "timeslot/timeslot_suggestion.html", context)


@permission_required("frontend.delete_appointment", raise_exception=True)
def appointment_delete(request):
    if request.method == "POST":
        if request.POST['action'] == "delete":
            for id in request.POST.getlist('select_row'):
                Appointment.objects.get(id=int(id)).delete()
            return HttpResponseRedirect(reverse('frontend:appointment_list'))


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
        for timeslot in Timeslot.objects.all():
            timeslot.update_count()
        return HttpResponseRedirect(reverse('frontend:appointment_list'))


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
        for timeslot in Timeslot.objects.all():
            timeslot.update_count()
        return HttpResponseRedirect(reverse('frontend:appointment_map'))


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


@permission_required("frontend.view_appointment", raise_exception=True)
def generate_pdf(request):
    vehicle_list = Area.objects.filter(is_parent=True)
    timeslot_list = Timeslot.objects.all().order_by("date")

    report = ReportLab("WBSA-Sammelliste", "Hendrik")
    report.write_titel("Sammel-Liste der WBSA")
    report.write_heading("Fahrzeuge:", 3)
    for vehicle in vehicle_list.all():
        report.write_bullet(vehicle.name)

    report.write_heading("Zeitfenster:", 3)
    for timeslot in timeslot_list.all():
        report.write_bullet(f"{timeslot.date}, von {timeslot.time_from} bis {timeslot.time_to}")
    report.new_page()

    for vehicle in vehicle_list.all():
        for timeslot in timeslot_list:
            appointment_list = Appointment.objects.filter(timeslot=timeslot, street__area__parent=vehicle).order_by("street")
            if appointment_list.count() == 0:
                continue
            report.write_heading(f"Fahzeug: {vehicle.name}", 2)
            report.write_heading(f"Zeitfenster: {timeslot.date}, {timeslot.time_from}-{timeslot.time_to} Uhr", 3)

            table_content = [["Name", "Adresse", "Bemerkung"]]
            for x in appointment_list.all():
                address = x.street.name + " " + x.house_number
                table_content.append((wrap_text(x.contact_name), wrap_text(address), wrap_text(x.text)))
            report.create_table(table_content)
            report.new_page()

    file = report.render()
    return FileResponse(open(file, "rb"), as_attachment=False)
