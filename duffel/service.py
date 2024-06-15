from django.conf import settings
import requests
from duffel_api import Duffel
from django.conf import settings
from django.http import JsonResponse
import logging

def get_duffel():
    return Duffel(access_token=settings.DUFFEL_ACCESS_TOKEN)

def get_airlines(after=None, limit=None):
    url = "https://api.duffel.com/air/airlines"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    if after is not None:
        params["after"] = after
        params["before"] = after
    if limit is not None:
        params["limit"] = limit
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_airline_by_id(id):
    url = f"https://api.duffel.com/air/airlines/{id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_aircrafts(after=None, limit=None):
    url = "https://api.duffel.com/air/aircraft"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    if after is not None:
        params["after"] = after
        params["before"] = after
    if limit is not None:
        params["limit"] = limit
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_aircraft_by_id(id):
    url = f"https://api.duffel.com/air/aircraft/{id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_airports(after=None, limit=None):
    url = "https://api.duffel.com/air/airports"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    if after is not None:
        params["after"] = after
        params["before"] = after
    if limit is not None:
        params["limit"] = limit
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_airport_by_id(id):
    url = f"https://api.duffel.com/air/airports/{id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_cities(after=None, limit=None):
    url = "https://api.duffel.com/air/cities"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    if after is not None:
        params["after"] = after
        params["before"] = after
    if limit is not None:
        params["limit"] = limit
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_city_by_id(id):
    url = f"https://api.duffel.com/air/cities/{id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_places(name=None, rad=None, lat=None, lng=None):
    url = "https://api.duffel.com/places/suggestions"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    if name is not None:
        params["name"] = name
    if rad is not None:
        params["rad"] = rad
    if lat is not None:
        params["lat"] = lat
    if lng is not None:
        params["lng"] = lng
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_offer_requests(after=None, limit=None):
    url = "https://api.duffel.com/air/offer_requests"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    if after is not None:
        params["after"] = after
        params["before"] = after
    if limit is not None:
        params["limit"] = limit
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()
    
def get_offer_request_by_id(id):
    url = f"https://api.duffel.com/air/offer_requests/{id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def create_duffel_offer_request(return_offers, supplier_timeout, slices, passengers, max_connections, cabin_class):
    url = f"https://api.duffel.com/air/offer_requests?return_offers={return_offers}&supplier_timeout={supplier_timeout}"
    
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"  # Use your Duffel access token
    }
    
    data = {
        "data": {
            "slices": slices,
            "passengers": passengers,
            "max_connections": max_connections,
            "cabin_class": cabin_class
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(e)
        return JsonResponse({'success': False, 'error': str(e), 'details': response.text}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        logging.error(e)
        return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': True, 'result': response.json()['data']})

def get_offers(after=None, limit=None, offer_request_id=None, max_connections=None, sort=None):
    url = "https://api.duffel.com/air/offers"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    if after is not None:
        params["after"] = after
        params["before"] = after
    if limit is not None:
        params["limit"] = limit
        
    params["offer_request_id"] = offer_request_id
    params["max_connections"] = max_connections
    params["sort"] = sort
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()
    
def get_offer_by_id(id):
    url = f"https://api.duffel.com/air/offers/{id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def update_passenger_details(offer_id, offer_passenger_id, loyalty_accounts, given_name, family_name):
    url = f"https://api.duffel.com/air/offers/{offer_id}/passengers/{offer_passenger_id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    data = {
        "data": {
            "loyalty_programme_accounts": loyalty_accounts,
            "given_name": given_name,
            "family_name": family_name
        }
    }

    response = requests.patch(url, json=data, headers=headers)
    return response.json()

def create_order(metadata, passengers , payments, selected_offers, order_type):
    url = f"https://api.duffel.com/air/orders"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    
    data = {
        "data": {
            "metadata": metadata,
            "passengers": passengers,
            "payments": payments,
            "selected_offers": selected_offers,
            "order_type": order_type
        }
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()

def get_orders(after=None, limit=None):
    url = "https://api.duffel.com/air/orders"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    if after is not None:
        params["after"] = after
        params["before"] = after
    if limit is not None:
        params["limit"] = limit
        
    response = requests.get(url, headers=headers, params=params)
    return response.json()
    
def get_order_by_id(id):
    url = f"https://api.duffel.com/air/orders/{id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()
    
def get_available_services_by_order_id(id):
    url = f"https://api.duffel.com/air/orders/{id}/available_services"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()
def add_service_to_order(id, payment, add_services):
    url = f"https://api.duffel.com/air/orders/{id}/services"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    
    data = {
        "data": {
            "payment": payment,
            "add_services": add_services
        }
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()

def update_order(id, meta):
    url = f"https://api.duffel.com/air/orders/{id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    
    data = {
        "data": {
            "metadata": meta
        }
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()

def create_payment(id, type, currency, amount):
    url = f"https://api.duffel.com/air/payments"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    
    data = {
        "data": {
            "payment": {
                "type": type,
                "currency": currency,
                "amount": amount
            },
            "order_id": id
        }
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()
    
def get_seats_by_order_id(id):
    url = f"https://api.duffel.com/air/orders/seat_maps?offer_id={id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_cancelled_orders(after=None, limit=None):
    url = "https://api.duffel.com/air/order_cancellations"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    if after is not None:
        params["after"] = after
        params["before"] = after
    if limit is not None:
        params["limit"] = limit
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def create_cancelled_orders(order_id):
    url = f"https://api.duffel.com/air/order_cancellations"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    
    data = {
        "data": {
            "order_id": order_id
        }
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()

def confirm_order_cancellation(order_resource_id):
    url = f"https://api.duffel.com/air/order_cancellations/{order_resource_id}/actions/confirm"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    
    data = {}

    response = requests.post(url, json=data, headers=headers)
    return response.json()

def get_order_cancellation(order_resource_id):
    url = f"https://api.duffel.com/air/order_cancellations/{order_resource_id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    
    params = {}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_order_change_request(id):
    url = f"https://api.duffel.com/air/order_change_requests/{id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    
    params = {}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

def create_order_change_request(order_id, slices, private_fares):
    url = f"https://api.duffel.com/air/order_change_requests"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    
    data = {
        "data": {
            "slices": slices,
            "private_fares": private_fares,
            "order_id": order_id
        }
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()

def get_order_change_offers(after=None, limit=None):
    url = "https://api.duffel.com/air/order_change_offers"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    params = {}
    if after is not None:
        params["after"] = after
        params["before"] = after
    if limit is not None:
        params["limit"] = limit
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_order_change_offer(id):
    url = f"https://api.duffel.com/air/order_change_offers/{id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    
    params = {}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

def create_pending_order_change(selected_order_change_offer):
    url = f"https://api.duffel.com/air/order_changes"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    
    data = {
        "data": {
            "selected_order_change_offer": selected_order_change_offer
        }
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()

def get_order_change(id):
    url = f"https://api.duffel.com/air/order_changes/{id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    
    params = {}

    response = requests.get(url, headers=headers, params=params)
    return response.json()


def confirm_order_change(payment, id):
    url = f"https://api.duffel.com/air/order_changes/{id}/actions/confirm"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    
    data = {
        "data": {
            "payment": payment
        }
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()

def create_batch_offer_request(supplier_timeout, slices, passengers, max_connections, cabin_class):
    url = f"https://api.duffel.com/air/batch_offer_requests?supplier_timeout={supplier_timeout}"
    
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"  # Use your Duffel access token
    }
    
    data = {
        "data": {
            "slices": slices,
            "passengers": passengers,
            "max_connections": max_connections,
            "cabin_class": cabin_class
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(e)
        return JsonResponse({'success': False, 'error': str(e), 'details': response.text}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        logging.error(e)
        return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': True, 'result': response.json()['data']})

def get_batch_offer_request(id):
    url = f"https://api.duffel.com/air/batch_offer_requests/{id}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}"
    }
    
    params = {}

    response = requests.get(url, headers=headers, params=params)
    return response.json()