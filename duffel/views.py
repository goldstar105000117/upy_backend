from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .decorator import require_auth
from .service import get_duffel, create_duffel_offer_request, get_offer_request_by_id, get_airlines, get_airline_by_id, get_aircrafts, get_aircraft_by_id, get_airports, get_airport_by_id, get_cities, get_city_by_id, get_places, get_offer_requests
import json

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_airlines_view(request):
    after = None
    limit = 50

    try:
        data = json.loads(request.body)
        after = data.get('after', after)
        limit = data.get('limit', limit)
    except json.JSONDecodeError:
        pass

    airlines_data = get_airlines(after=after, limit=limit)

    if not airlines_data:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)

    return JsonResponse({'success': True, 'result': airlines_data})
    # airlines_data = []

    # if 'data' in response:
    #     for airline in response['data']:
    #         print(airline)
    #         # if airline.get('logo_symbol_url') is not None and airline.get('conditions_of_carriage_url') is not None:
    #         airlines_data.append({
    #             'id': airline.get('id', 'No ID'),
    #             'name': airline.get('name', 'No Name'),  
    #             'iata_code': airline.get('iata_code', 'No IATA Code'),  
    #             'logo_symbol_url': airline.get('logo_symbol_url', 'No Logo Symbol URL'),  
    #             'conditions_of_carriage_url': airline.get('conditions_of_carriage_url', 'No Conditions of Carriage URL'),  
    #         })
    # else:
    #     return JsonResponse({'success': False, 'error': 'Failed to retrieve data'})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_airline_view(request, pk):
    airlines_data = get_airline_by_id(id=pk)

    if not airlines_data:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)

    return JsonResponse({'success': True, 'result': airlines_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_aircrafts_view(request):
    after = None
    limit = 50

    try:
        data = json.loads(request.body)
        after = data.get('after', after)
        limit = data.get('limit', limit)
    except json.JSONDecodeError:
        pass

    aircrafts_data = get_aircrafts(after=after, limit=limit)

    if not aircrafts_data:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)

    return JsonResponse({'success': True, 'result': aircrafts_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_aircraft_view(request, pk):
    aircrafts_data = get_aircraft_by_id(id=pk)

    if not aircrafts_data:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)

    return JsonResponse({'success': True, 'result': aircrafts_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_airports_view(request):
    after = None
    limit = 50

    try:
        data = json.loads(request.body)
        after = data.get('after', after)
        limit = data.get('limit', limit)
    except json.JSONDecodeError:
        pass

    airports_data = get_airports(after=after, limit=limit)

    if not airports_data:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)

    return JsonResponse({'success': True, 'result': airports_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_airport_view(request, pk):
    airports_data = get_airport_by_id(id=pk)

    if not airports_data:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)

    return JsonResponse({'success': True, 'result': airports_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_cities_view(request):
    after = None
    limit = 50

    try:
        data = json.loads(request.body)
        after = data.get('after', after)
        limit = data.get('limit', limit)
    except json.JSONDecodeError:
        pass

    response = get_cities(after=after, limit=limit)

    cities_data = []
    if 'data' in response:
        for city in response['data']:
            cities_data.append({
                'id': city.get('id', 'No ID'),
                'name': city.get('name', 'No Name'),  
                'iata_country_code': city.get('iata_country_code', 'No IATA Country Code'),  
                'iata_code': city.get('iata_code', 'No IATA Code'),  
            })
    else:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)
        
    return JsonResponse({'success': True, 'result': {'meta': response['meta'], 'data': cities_data}})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_city_view(request, pk):
    response = get_city_by_id(id=pk)

    cities_data = []
    if 'data' in response:
        cities_data.append({
            'id': response['data'].get('id', 'No ID'),
            'name': response['data'].get('name', 'No Name'),  
            'iata_country_code': response['data'].get('iata_country_code', 'No IATA Country Code'),  
            'iata_code': response['data'].get('iata_code', 'No IATA Code'),  
        })
    else:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)
        
    return JsonResponse({'success': True, 'result': cities_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_places_view(request):
    name=None
    rad=None
    lat=None
    lng=None

    try:
        data = json.loads(request.body)
        name = data.get('name', name)
        rad = data.get('rad', rad)
        lat = data.get('lat', lat)
        lng = data.get('lng', lng)
    except json.JSONDecodeError:
        pass
    place_data = get_places(name=name, rad=rad, lat=lat, lng=lng)

    if not place_data:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)

    return JsonResponse({'success': True, 'result': place_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_offer_requests_view(request):
    after = None
    limit = 50

    try:
        data = json.loads(request.body)
        after = data.get('after', after)
        limit = data.get('limit', limit)
    except json.JSONDecodeError:
        pass

    offer_requests_data = get_offer_requests(after=after, limit=limit)

    if not offer_requests_data:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)

    return JsonResponse({'success': True, 'result': offer_requests_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def create_offer_request_view(request):
    try:
        data = json.loads(request.body)

        slices = data.get('slices')
        passengers = data.get('passengers')
        max_connections = data.get('max_connections')
        cabin_class = data.get('cabin_class')
        
        response = create_duffel_offer_request('true', 10000, slices=slices, passengers=passengers, max_connections=max_connections, cabin_class=cabin_class)
        return response
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except KeyError as e:
        return JsonResponse({'success': False, 'error': f'Missing key {e}'}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_offer_request_view(request, pk):
    offer_request_data = get_offer_request_by_id(id=pk)
    if offer_request_data.get('errors'):
        return JsonResponse({'success': False, 'error': offer_request_data['errors'][0]['title']}, status=404)
    return JsonResponse({'success': True, 'result': offer_request_data})