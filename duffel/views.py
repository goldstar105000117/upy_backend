from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .decorator import require_auth
from .service import get_airlines, get_airline_by_id
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