from django.urls import path
from django.views.generic.base import RedirectView
from . import views, auth_views
from .view_collection.area import AreaListView
from .view_collection.street import StreetListView
from .view_collection.timeslot import TimeslotListView
from .view_collection.appointment import AppointmentListView, UpdateAppointmentCollected
from .view_collection.collect import CollectMenu, CollectList

app_name = 'frontend'
urlpatterns = [
    path('', RedirectView.as_view(url='appointment/map'), name='index'),
    path('area/list', AreaListView.as_view(), name='area_list'),
    path('area/new', views.area_new, name='area_new'),
    path('area/delete', views.area_delete, name='area_delete'),
    path('area/<int:area_id>', views.area_view, name='area_view'),
    path('area/<int:area_id>/edit', views.area_edit, name='area_edit'),
    path('street/list', StreetListView.as_view() , name='street_list'),
    path('street/delete', views.street_delete, name='street_delete'),
    path('street/bulkadd', views.street_bulkadd, name='street_bulkadd'),
    path('street/osm_import', views.street_osm_import, name='street_osm_import'),
    path('street/<int:street_id>/edit', views.street_edit, name='street_edit'),
    path('timeslot/list', TimeslotListView.as_view(), name='timeslot_list'),
    path('timeslot/delete', views.timeslot_delete, name='timeslot_delete'),
    path('timeslot/new', views.timeslot_new, name='timeslot_new'),
    path('timeslot/<int:timeslot_id>/edit', views.timeslot_edit, name='timeslot_edit'),
    path('timeslot/suggestion', views.timeslot_suggestion, name='timeslot_suggestion'),
    path('appointment/list', AppointmentListView.as_view(), name='appointment_list'),
    path('appointment/pdf', views.generate_pdf, name='appointment_pdf'),
    path('appointment/delete', views.appointment_delete, name='appointment_delete'),
    path('appointment/map', views.appointment_map, name='appointment_map'),
    path('appointment/new', views.appointment_new, name='appointment_new'),
    path('appointment/<int:appointment_id>', views.appointment_view, name='appointment_view'),
    path('appointment/<int:appointment_id>/edit', views.appointment_edit, name='appointment_edit'),
    path('appointment/<int:appointment_id>/collected', UpdateAppointmentCollected.as_view()),
    path('mobile/menu', CollectMenu.as_view(), name='collect_menu'),
    path('mobile/list', CollectList.as_view(), name='collect_list'),
    path('auth/login', auth_views.login_user, name='login'),
    path('auth/logout', auth_views.logout_user, name='logout')
]
