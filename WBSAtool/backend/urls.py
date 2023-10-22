from django.urls import path
from rest_framework.authtoken import views as drf_views
from backend import views

app_name = 'backend'
urlpatterns = [
    path('area', views.AreaList.as_view()),
    path('area/<int:pk>', views.AreaDetail.as_view()),
    path('street', views.StreetList.as_view()),
    path('street/<int:pk>', views.StreetDetail.as_view()),
    path('timeslot', views.TimeslotList.as_view()),
    path('timeslot/<int:pk>', views.TimeslotDetail.as_view()),
    path('appointment', views.AppointmentList.as_view()),
    path('appointment/<int:pk>', views.AppointmentDetail.as_view()),
    path('api-token-auth/', drf_views.obtain_auth_token)
]