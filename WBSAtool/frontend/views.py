from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Area, Street, Timeslot, Appointment


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def area_list(request):
    AreaList = Area.objects.all()
    context = {'area_list': AreaList}
    return render(request, 'area/area_list.html', context)


def area_view(request, area_id):
    area = get_object_or_404(Area, id=area_id)
    if area.is_parent:
        AreaList = Area.objects.filter(parent=area)
        StreetList = []
        for subarea in AreaList:
            l = Street.objects.filter(area=subarea)
            for street in l:
                StreetList.append(street)
        print(StreetList)
    else:
        StreetList = Street.objects.filter(area=area)
    context = {'area': area, 'street_list': StreetList}
    return render(request, 'area/area_view.html', context)


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
        # return HttpResponseRedirect(reverse('wbsa:area_list', args=(area.id,)))


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
    StreetList = Street.objects.all()
    context = {'street_list': StreetList}
    return render(request, 'street/street_list.html', context)


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
        for street in request.POST['data'].split("\r\n"):
            newStreet = Street(name=street)
            newStreet.save()
        return HttpResponseRedirect(reverse('wbsa:street_list'))

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
    return HttpResponse("noch nicht implementiert")


def appointment_new(request):
    if request.method == 'GET':
        StreetList = Street.objects.all()
        TimeslotList = Timeslot.objects.all()
        context = {"street_list": StreetList, 'timeslot_list': TimeslotList}
        return render(request, 'appointment/appointment_edit.html', context)
