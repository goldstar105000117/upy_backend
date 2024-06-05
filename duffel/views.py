from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .decorator import require_auth
from .service import get_airlines, get_airline_by_id, get_aircrafts, get_aircraft_by_id, get_airports, get_airport_by_id, get_cities
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