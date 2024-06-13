from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .decorator import require_auth
from .service import get_duffel, get_order_cancellation, get_order_change_request, confirm_order_cancellation, create_cancelled_orders, get_cancelled_orders, get_seats_by_order_id, add_service_to_order, update_order,create_payment, get_orders, get_order_by_id, get_available_services_by_order_id, create_order, update_passenger_details, get_offers, get_offer_by_id, create_duffel_offer_request, get_offer_request_by_id, get_airlines, get_airline_by_id, get_aircrafts, get_aircraft_by_id, get_airports, get_airport_by_id, get_cities, get_city_by_id, get_places, get_offer_requests
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

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_offers_view(request):
    after = None
    limit = 50
    sort = 'total_amount'
    max_connections = 2

    try:
        data = json.loads(request.body)
        after = data.get('after', after)
        limit = data.get('limit', limit)
        sort = data.get('sort', sort)
        max_connections = data.get('max_connections', max_connections)
        offer_request_id = data.get('offer_request_id', None)
        
        if not offer_request_id:
            return JsonResponse({'success': False, 'error': 'Missing offer_request_id'}, status=400)
    except json.JSONDecodeError:
        pass

    offers_data = get_offers(after=after, limit=limit, offer_request_id=offer_request_id, sort=sort, max_connections=max_connections)

    if not offers_data:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)

    return JsonResponse({'success': True, 'result': offers_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_offer_view(request, pk):
    offer_data = get_offer_by_id(id=pk)
    if offer_data.get('errors'):
        return JsonResponse({'success': False, 'error': offer_data['errors'][0]['title']}, status=404)
    return JsonResponse({'success': True, 'result': offer_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def update_passenger_details_view(request):
    try:
        data = json.loads(request.body)
        offer_id = data.get('offer_id', None)
        offer_passenger_id = data.get('offer_passenger_id', None)
        loyalty_accounts = data.get('loyalty_accounts', [])
        given_name = data.get('given_name', '')
        family_name = data.get('family_name', '')
        print(offer_id, offer_passenger_id)
        if not offer_id or offer_id == '':
            return JsonResponse({'success': False, 'error': 'Missing offer_id'}, status=400)
        if not offer_passenger_id or offer_passenger_id == '':
            return JsonResponse({'success': False, 'error': 'Missing offer_passenger_id'}, status=400)
    except json.JSONDecodeError as e:
        return JsonResponse({'success': False, 'error': e}, status=400)

    passenger_details_data = update_passenger_details(offer_id=offer_id, offer_passenger_id=offer_passenger_id, loyalty_accounts=loyalty_accounts, given_name=given_name, family_name=family_name)
    
    if passenger_details_data.get('errors'):
        return JsonResponse({'success': False, 'error': passenger_details_data['errors'][0]['title']}, status=404)

    return JsonResponse({'success': True, 'result': passenger_details_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def create_order_view(request):
    try:
        data = json.loads(request.body)
        metadata = data.get('metadata', None)
        passengers = data.get('passengers')
        if not passengers or not isinstance(passengers, list):
            return JsonResponse({'success': False, 'error': 'Invalid or missing passengers data'}, status=400)
        
        for passenger in passengers:
            required_fields = ['id', 'given_name', 'family_name', 'email', 'phone_number']
            for field in required_fields:
                if not passenger.get(field):
                    return JsonResponse({'success': False, 'error': f'Missing {field} in passenger data'}, status=400)

        payments = data.get('payments')
        if not payments or not isinstance(payments, list) or not all('type' in payment and 'amount' in payment and 'currency' in payment for payment in payments):
            return JsonResponse({'success': False, 'error': 'Invalid or missing payments data'}, status=400)
        
        selected_offers = data.get('selected_offers')
        if not selected_offers or not isinstance(selected_offers, list) or not all(isinstance(offer, str) for offer in selected_offers):
            return JsonResponse({'success': False, 'error': 'Invalid or missing selected offers data'}, status=400)

        order_type = data.get('type')
        if not order_type or not isinstance(order_type, str):
            return JsonResponse({'success': False, 'error': 'Invalid or missing type data'}, status=400)

    except json.JSONDecodeError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

    order_data = create_order(metadata=metadata, passengers=passengers, payments=payments, selected_offers=selected_offers, order_type=order_type)
    if order_data.get('errors'):
        return JsonResponse({'success': False, 'error': order_data}, status=404)

    return JsonResponse({'success': True, 'result': order_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_orders_view(request):
    after = None
    limit = 50

    try:
        data = json.loads(request.body)
        after = data.get('after', after)
        limit = data.get('limit', limit)
    except json.JSONDecodeError:
        pass

    orders_data = get_orders(after=after, limit=limit)

    if not orders_data:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)

    return JsonResponse({'success': True, 'result': orders_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_order_view(request, pk):
    order_data = get_order_by_id(id=pk)
    if order_data.get('errors'):
        return JsonResponse({'success': False, 'error': order_data['errors'][0]['title']}, status=404)
    return JsonResponse({'success': True, 'result': order_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_available_services_view(request, pk):
    available_services_data = get_available_services_by_order_id(id=pk)
    if available_services_data.get('errors'):
        return JsonResponse({'success': False, 'error': available_services_data['errors'][0]['title']}, status=404)
    return JsonResponse({'success': True, 'result': available_services_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def add_service_to_order_view(request, pk):
    try:
        data = json.loads(request.body)
        payment = data.get('payment')
        if not payment:
            return JsonResponse({'success': False, 'error': 'Invalid or missing payment data'}, status=400)

        add_services = data.get('add_services')
        if not add_services:
            return JsonResponse({'success': False, 'error': 'Invalid or missing services data'}, status=400)
        
    except json.JSONDecodeError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

    service_data = add_service_to_order(id=pk, payment=payment, add_services=add_services)
    if service_data.get('errors'):
        return JsonResponse({'success': False, 'error': service_data}, status=404)

    return JsonResponse({'success': True, 'result': service_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def update_order_view(request, pk):
    try:
        data = json.loads(request.body)
        meta = data.get('meta')
        if not meta:
            return JsonResponse({'success': False, 'error': 'Invalid or missing meta data'}, status=400)
        
    except json.JSONDecodeError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

    order_data = update_order(id=pk, meta=meta)
    if order_data.get('errors'):
        return JsonResponse({'success': False, 'error': order_data}, status=404)

    return JsonResponse({'success': True, 'result': order_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def create_payment_view(request, pk):
    try:
        data = json.loads(request.body)
        type = data.get('type')
        if not type:
            return JsonResponse({'success': False, 'error': 'Invalid or missing type data'}, status=400)
        
        currency = data.get('currency')
        if not currency:
            return JsonResponse({'success': False, 'error': 'Invalid or missing currency data'}, status=400)
        
        amount = data.get('amount')
        if not amount:
            return JsonResponse({'success': False, 'error': 'Invalid or missing amount data'}, status=400)
        
    except json.JSONDecodeError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

    order_data = create_payment(id=pk, type=type, currency=currency, amount=amount)
    
    if order_data.get('errors'):
        return JsonResponse({'success': False, 'error': order_data}, status=404)

    return JsonResponse({'success': True, 'result': order_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_seats_view(request, pk):
    seats_data = get_seats_by_order_id(id=pk)
    if seats_data.get('errors'):
        return JsonResponse({'success': False, 'error': seats_data['errors'][0]['title']}, status=404)
    return JsonResponse({'success': True, 'result': seats_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_cancelled_orders_view(request):
    after = None
    limit = 50

    try:
        data = json.loads(request.body)
        after = data.get('after', after)
        limit = data.get('limit', limit)
    except json.JSONDecodeError:
        pass

    cancelled_orders_data = get_cancelled_orders(after=after, limit=limit)

    if not cancelled_orders_data:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)

    return JsonResponse({'success': True, 'result': cancelled_orders_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def create_cancelled_orders_view(request):
    order_id = None
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id', order_id)
        if not order_id:
            return JsonResponse({'success': False, 'error': 'Invalid or missing order id data'}, status=400)
    except json.JSONDecodeError:
        pass

    create_cancelled_orders_data = create_cancelled_orders(order_id=order_id)

    if not create_cancelled_orders_data:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)

    return JsonResponse({'success': True, 'result': create_cancelled_orders_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def confirm_order_cancellation_view(request):
    order_resource_id = None
    try:
        data = json.loads(request.body)
        order_resource_id = data.get('order_resource_id', order_resource_id)
        if not order_resource_id:
            return JsonResponse({'success': False, 'error': 'Invalid or missing order resource id data'}, status=400)
    except json.JSONDecodeError:
        pass

    confirm_order_cancellation_data = confirm_order_cancellation(order_resource_id=order_resource_id)

    if not confirm_order_cancellation_data:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)

    return JsonResponse({'success': True, 'result': confirm_order_cancellation_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_order_cancellation_view(request):
    order_resource_id = None
    try:
        data = json.loads(request.body)
        order_resource_id = data.get('order_resource_id', order_resource_id)
        if not order_resource_id:
            return JsonResponse({'success': False, 'error': 'Invalid or missing order resource id data'}, status=400)
    except json.JSONDecodeError:
        pass

    order_cancellation_data = get_order_cancellation(order_resource_id=order_resource_id)

    if not order_cancellation_data:
        return JsonResponse({'success': False, 'error': 'No data found'}, status=404)

    return JsonResponse({'success': True, 'result': order_cancellation_data})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_order_change_request_view(request, pk):
    order_change_request_data = get_order_change_request(id=pk)
    if order_change_request_data.get('errors'):
        return JsonResponse({'success': False, 'error': order_change_request_data['errors'][0]['title']}, status=404)
    return JsonResponse({'success': True, 'result': order_change_request_data})