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
    path('offers/', views.get_offers_view, name='get_offers'),
    path('offers/<str:pk>/', views.get_offer_view, name='get_offer'),
    path('offers/passenger/update/', views.update_passenger_details_view, name='update_passenger_details'),
    path('orders/create/', views.create_order_view, name='create_order'),
    path('orders/', views.get_orders_view, name='get_orders'),
    path('orders/<str:pk>/', views.get_order_view, name='get_order'),
    path('orders/<str:pk>/available_services/', views.get_available_services_view, name='get_available_services'),
    path('orders/<str:pk>/add_service/', views.add_service_to_order_view, name='add_service_to_order'),
    path('orders/<str:pk>/update/', views.update_order_view, name='update_order'),
    path('orders/<str:pk>/payment/', views.create_payment_view, name='create_payment'),
    path('orders/<str:pk>/seats/', views.get_seats_view, name='get_seats'),
    path('orders/cancelled/', views.get_cancelled_orders_view, name='get_cancelled_orders'),
    path('orders/cancelled/create/', views.create_cancelled_orders_view, name='create_cancelled_orders'),
    path('orders/cancelled/confirm/', views.confirm_order_cancellation_view, name='confirm_order_cancellation'),
    path('orders/cancelled/get/', views.get_order_cancellation_view, name='get_order_cancellation'),
    path('orders/change/request/', views.create_order_change_request_view, name='create_order_change_request'),
    path('orders/change/request/<str:pk>/', views.get_order_change_request_view, name='get_order_change_request'),
    path('orders/change/create/', views.create_pending_order_change_view, name='create_pending_order_change'),
    path('orders/change/confirm/', views.confirm_order_change_view, name='confirm_order_change'),
    path('orders/change/<str:pk>/', views.get_order_change_view, name='get_order_change'),
    path('orders/offer/', views.get_order_change_offers_view, name='get_order_change_offers'),
    path('orders/offer/<str:pk>/', views.get_order_change_offer_view, name='get_order_change_offer'),
    path('batch_offer_request/create/', views.create_batch_offer_request_view, name='create_batch_offer_request'),
    path('batch_offer_request/<str:pk>/', views.get_batch_offer_request_view, name='get_batch_offer_request'),
    path('airline_changes/', views.get_airline_changes_view, name='get_airline_changes'),
    path('airline_changes/<str:pk>/', views.update_airline_change_view, name='update_airline_change'),
    path('airline_changes/<str:pk>/accept/', views.accept_airline_change_view, name='accept_airline_change'),
    path('stays/search/', views.search_accommodation_view, name='search_accommodation'),
    path('customer/', views.get_customer_view, name='get_customer'),
    path('customer/create/', views.create_customer_view, name='create_customer'),
    path('customer/update/', views.update_customer_view, name='update_customer'),
]
