from django.urls import path

from . import views

app_name = 'wbsa'
urlpatterns = [
    path('', views.index, name='index'),
    path('area/list', views.area_list, name='area_list'),
    path('area/<int:area_id>', views.area_view, name='area_view'),
    path('area/new', views.area_new, name='area_new'),
    path('area/<int:area_id>/edit', views.area_edit, name='area_edit'),
    path('street/list', views.street_list, name='street_list'),
    path('street/<int:street_id>/edit', views.street_edit, name='street_edit'),
    path('street/bulkadd', views.street_bulkadd, name='street_bulkadd'),
    path('timeslot/list', views.timeslot_list, name='timeslot_list'),
    path('appointment/list', views.appointment_list, name='appointment_list'),
    path('appointment/<int:appointment_id>', views.appointment_view, name='appointment_view'),
    path('appointment/<int:appointment_id>/edit', views.appointment_edit, name='appointment_edit'),
    path('appointment/new', views.appointment_new, name='appointment_new'),
]
