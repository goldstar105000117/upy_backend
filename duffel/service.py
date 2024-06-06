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