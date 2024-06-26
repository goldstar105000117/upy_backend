# constants.py

URL_DESCRIPTIONS = {
    "duffel/airlines/": "list airlines",
    "duffel/airlines/<str:pk>/": "single airline",
    "duffel/aircraft/": "list aircrafts",
    "duffel/aircraft/<str:pk>/": "single aircraft",
    "duffel/airport/": "list airports",
    "duffel/airport/<str:pk>/": "single airport",
    "duffel/cities/": "list cities",
    "duffel/cities/<str:pk>/": "single city",
    "duffel/places/": "list place suggestions",
    "duffel/offer_request/": "list offer requests",
    "duffel/offer_request/create/": "create offer request",
    "duffel/offer_request/<str:pk>/": "single offer request",
    "duffel/offers/": "list offers",
    "duffel/offers/<str:pk>/": "single offer",
    "duffel/offers/passenger/update/": "update single offer passenger",
    "duffel/orders/": "list orders",
    "duffel/orders/create/": "create order",
    "duffel/orders/<str:pk>/": "single orders",
    "duffel/orders/<str:pk>/available_services/": "list available services for order",
    "duffel/orders/<str:pk>/add_service/": "add service to order",
    "duffel/orders/<str:pk>/update/": "update single order",
    "duffel/orders/<str:pk>/payment/": "create payment",
    "duffel/orders/<str:pk>/seats/": "seat maps",
    "duffel/orders/cancelled/": "list order cancellations",
    "duffel/orders/cancelled/create/": "create pending order cancellation",
    "duffel/orders/cancelled/confirm/": "confirm order cancellation",
    "duffel/orders/cancelled/get/": "single order cancellation",
    "duffel/orders/change/request/": "create order change request",
    "duffel/orders/change/request/<str:pk>/": "single order change request",
    "duffel/orders/change/create/": "create pending order change",
    "duffel/orders/change/confirm/": "confirm order change",
    "duffel/orders/change/<str:pk>/": "single order change",
    "duffel/orders/offers/": "list order change offers",
    "duffel/orders/offers/<str:pk>/": "single order change offer",
    "duffel/batch_offer_request/create/": "create batch offer request",
    "duffel/batch_offer_request/<str:pk>/": "single batch offer request",
    "duffel/airline_changes/": "list airline-initiated changes",
    "duffel/airline_changes/<str:pk>/": "update airline-initiated change",
    "duffel/airline_changes/<str:pk>/accept/": "accept airline-initiated change",
    "duffel/stays/search/": "search",
}
