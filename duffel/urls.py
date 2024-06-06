from django.urls import path
from . import views

urlpatterns = [
    path('airlines/', views.get_airlines_view, name='get_airlines'),
    path('airlines/<str:pk>/', views.get_airline_view, name='get_airline_by_id'),
    path('aircraft/', views.get_aircrafts_view, name='get_aircrafts'),
    path('aircraft/<str:pk>/', views.get_aircraft_view, name='get_aircraft_by_id'),
    path('airport/', views.get_airports_view, name='get_airports'),
    path('airport/<str:pk>/', views.get_airport_view, name='get_airport_by_id'),
    path('cities/', views.get_cities_view, name='get_cities'),
    path('cities/<str:pk>/', views.get_city_view, name='get_cities_by_id'),
    path('places/', views.get_places_view, name='get_places'),
    path('offer_request/', views.get_offer_requests_view, name='get_offer_requests'),
    path('offer_request/create/', views.create_offer_request_view, name='create_offer_request'),
    path('offer_request/<str:pk>/', views.get_offer_request_view, name='get_offer_request'),
]
