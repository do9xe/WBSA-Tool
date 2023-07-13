from django.urls import path
from django.views.generic.base import RedirectView
from . import views

app_name = 'wbsa'
urlpatterns = [
    path('', RedirectView.as_view(url='appointment/map'), name='index'),
    path('area/list', views.area_list, name='area_list'),
    path('area/new', views.area_new, name='area_new'),
    path('area/<int:area_id>', views.area_view, name='area_view'),
    path('area/<int:area_id>/edit', views.area_edit, name='area_edit'),
    path('street/list', views.street_list, name='street_list'),
    path('street/bulkadd', views.street_bulkadd, name='street_bulkadd'),
    path('street/osm_import', views.street_osm_import, name='street_osm_import'),
    path('street/<int:street_id>/edit', views.street_edit, name='street_edit'),
    path('timeslot/list', views.timeslot_list, name='timeslot_list'),
    path('timeslot/new', views.timeslot_new, name='timeslot_new'),
    path('timeslot/<int:timeslot_id>/edit', views.timeslot_edit, name='timeslot_edit'),
    path('timeslot/suggestion', views.timeslot_suggestion, name='timeslot_suggestion'),
    path('appointment/list', views.appointment_list, name='appointment_list'),
    path('appointment/map', views.appointment_map, name='appointment_map'),
    path('appointment/new', views.appointment_new, name='appointment_new'),
    path('appointment/<int:appointment_id>', views.appointment_view, name='appointment_view'),
    path('appointment/<int:appointment_id>/edit', views.appointment_edit, name='appointment_edit'),
]
