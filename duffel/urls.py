from django.urls import path
from . import views

urlpatterns = [
    path('airlines/', views.get_airlines_view, name='get_airlines'),
    path('airlines/<str:pk>/', views.get_airline_view, name='get_airline_by_id'),
    path('aircraft/', views.get_aircrafts_view, name='get_aircrafts'),
    path('aircraft/<str:pk>/', views.get_aircraft_view, name='get_aircraft_by_id'),
]
