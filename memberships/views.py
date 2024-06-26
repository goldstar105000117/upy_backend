from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from authentication.decorator import require_auth
# from .service import 
import json
import re
from .convex import get_plans, create_plan, update_plan

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_plans_view(request):
    result = get_plans()
    
    if not result:
        return JsonResponse({'success': False, 'error': 'Failed to get plan data'}, status=500)  

    return JsonResponse({'success': True, 'result': result})

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def create_plan_view(request):
    try:
        data = json.loads(request.body)
        type = data.get('type')
        price = data.get('price')
        billing_period = data.get('billing_period')
        discount = data.get('discount')
        storage = data.get('storage')
        token = data.get('token')
        
        if not type:
            return JsonResponse({'success': False, 'error': 'Invalid or missing type data'}, status=400)
        
        if not price:
            return JsonResponse({'success': False, 'error': 'Invalid or missing price data'}, status=400)
        
        if not billing_period:
            return JsonResponse({'success': False, 'error': 'Invalid or missing billing period data'}, status=400)
        
        if not discount and discount != 0:
            return JsonResponse({'success': False, 'error': 'Invalid or missing discount data'}, status=400)
        
        if not storage:
            return JsonResponse({'success': False, 'error': 'Invalid or missing storage data'}, status=400)
        
        if not token:
            return JsonResponse({'success': False, 'error': 'Invalid or missing token data'}, status=400)

    except json.JSONDecodeError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    plan_data = create_plan(type=type, price=price, billing_period=billing_period, discount=discount, storage=storage, token=token)
    if not plan_data:
        return JsonResponse({'success': False, 'error': 'Failed to create new plan.'}, status=500)    

    return JsonResponse({'success': True, 'result': {'type': type, 'price': price, 'billing_period': billing_period, 'discount': discount, 'storage': storage, 'token': token, 'is_active': True, 'id': plan_data['result']}})


@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def update_plan_view(request, pk):
    try:
        data = json.loads(request.body)
        type = data.get('type')
        price = data.get('price')
        billing_period = data.get('billing_period')
        discount = data.get('discount')
        storage = data.get('storage')
        token = data.get('token')
        
        if not type:
            return JsonResponse({'success': False, 'error': 'Invalid or missing type data'}, status=400)
        
        if not price:
            return JsonResponse({'success': False, 'error': 'Invalid or missing price data'}, status=400)
        
        if not billing_period:
            return JsonResponse({'success': False, 'error': 'Invalid or missing billing period data'}, status=400)
        
        if not discount and discount != 0:
            return JsonResponse({'success': False, 'error': 'Invalid or missing discount data'}, status=400)
        
        if not storage:
            return JsonResponse({'success': False, 'error': 'Invalid or missing storage data'}, status=400)
        
        if not token:
            return JsonResponse({'success': False, 'error': 'Invalid or missing token data'}, status=400)

    except json.JSONDecodeError:
        pass
    
    plan_data = update_plan(id=pk, type=type, price=price, billing_period=billing_period, discount=discount, storage=storage, token=token)
    
    if plan_data['success']:
        return JsonResponse({'success': True, 'result': {'type': type, 'price': price, 'billing_period': billing_period, 'discount': discount, 'storage': storage, 'token': token, 'is_active': True, 'id': plan_data['result']}})
    
    return JsonResponse({'success': False, 'error': 'Failed to update plan.'}, status=500)    
