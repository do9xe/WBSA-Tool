from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Area, Street, Timeslot, Appointment


def area_list(request):
    if request.method == 'GET':
        AreaList = Area.objects.all()
        context = {'area_list': AreaList}
        return render(request, 'area/area_list.html', context)
    if request.method == 'POST':
        if request.POST['action'] == "delete_areas":
            for id in request.POST.getlist('select_row'):
                Area.objects.get(id=int(id)).delete()
            return HttpResponseRedirect(reverse('wbsa:area_list'))
        elif request.POST['action']:
            id = int(request.POST['action'])
            Area.objects.get(id=id).delete()
            return HttpResponseRedirect(reverse('wbsa:area_list'))


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


def area_new(request):
    if request.method == 'GET':
        area = {}
        area['name'] = "new Area"
        AreaList = Area.objects.filter(is_parent=True)
        context = {'area': area, 'parent_area_list': AreaList}
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


def street_list(request):
    if request.method == 'GET':
        StreetList = Street.objects.all()
        context = {'street_list': StreetList}
        return render(request, 'street/street_list.html', context)
    if request.method == 'POST':
        if request.POST['action'] == "delete":
            for id in request.POST.getlist('select_row'):
                Street.objects.get(id=int(id)).delete()
            return HttpResponseRedirect(reverse('wbsa:street_list'))


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


def timeslot_list(request):
    TimeslotList = Timeslot.objects.all()
    context = {'timeslot_list': TimeslotList}
    return render(request, 'timeslot/timeslot_list.html', context)


def appointment_list(request):
    AppointmentList = Appointment.objects.all()
    context = {'appointment_list': AppointmentList}
    return render(request, 'appointment/appointment_list.html', context)


def appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.GET['format'] == "modal":
        context = {'appointment': appointment}
        return render(request, 'appointment/appointment_modal.html', context)


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
        appointment.text = ""
        appointment.phone = request.POST['phone']
        appointment.email = request.POST['email']
        appointment.save()
        return HttpResponseRedirect(reverse('wbsa:appointment_list'))


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
        text = ""
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

def appointment_map(request):
    AppointmentList = Appointment.objects.all()
    context = {'appointment_list': AppointmentList}
    return render(request, 'appointment/map.html', context)
