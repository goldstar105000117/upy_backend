from django.conf import settings
import requests

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