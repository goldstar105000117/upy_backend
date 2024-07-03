from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from authentication.decorator import require_auth
# from .service import 
import json
from .convex import get_plans, create_plan, update_user_plan_plan_id, set_expires_at, update_plan, get_customer, activate_plan, activate_user_plan,delete_user_plan, deactivate_plan, get_plan_by_id, get_user_plans, get_user_plan, get_user_plan_by_plan_id, get_stripe_customer_from_user_id, create_customer, create_user_plan
from memberships import stripe_api
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from django.utils import timezone as django_timezone

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
        product_id = data.get('product_id')
        
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
        
        if not product_id:
            return JsonResponse({'success': False, 'error': 'Invalid or missing product id data'}, status=400)

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

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def activate_plan_view(request, pk):
    plan_data = activate_plan(id=pk)
    
    if plan_data['success']:
        return JsonResponse({'success': True, 'result': plan_data})
    
    return JsonResponse({'success': False, 'error': 'Failed to activate plan.'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def deactivate_plan_view(request, pk):
    plan_data = deactivate_plan(id=pk)
    
    if plan_data['success']:
        return JsonResponse({'success': True, 'result': plan_data})
    
    return JsonResponse({'success': False, 'error': 'Failed to deactivate plan.'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def create_stripe_payment_intent_view(request):
    try:
        data = json.loads(request.body)
        plan_id = data.get('plan_id')
        
        if not plan_id:
            return JsonResponse({'success': False, 'error': 'Invalid or missing plan id data'}, status=400)

    except json.JSONDecodeError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    plan = get_plan_by_id(id=plan_id)
    if not plan:
        return JsonResponse({'success': False, 'error': 'Invalid plan'}, status=400)
    
    user_plan = get_user_plan_by_plan_id(plan_id=plan_id, user_id=request.user['_id'], complete=False)
    
    stripe_customer = get_stripe_customer_from_user_id(user_id=request.user['_id'])
    
    if not stripe_customer:
        customer = stripe_api.create_customer(email=request.user['email'])
        customer_id = customer.id
        
        customer_data = create_customer(customer_id=customer_id, user_id=request.user['_id'])
        if not customer_data['success']:
            return JsonResponse({'success': False, 'error': 'Failed to create new customer.'}, status=500)  
    else:
        customer_id = stripe_customer[0]['customer_id']
        
    is_trial = False

    if not user_plan:
        subscription = stripe_api.create_subscription(
            customer_id=customer_id,
            product_id=plan[0]['product_id'],
            email=request.user['email'],
        )

        user_plan_data = create_user_plan(plan_id=plan_id, user_id=request.user['_id'], provider_id=subscription['subscription_id'], status=subscription['status'])
        
        if not user_plan_data['success']:
            return JsonResponse({'success': False, 'error': 'Failed to create new user plan.'}, status=500)  
        
        client_secret = subscription['client_secret']
        is_trial = subscription['is_trial']
    else:
        creation_time = datetime.fromtimestamp(user_plan[0]['_creationTime'] / 1000, tz=timezone.utc)

        current_time_minus_22_hours = django_timezone.now() - relativedelta(hours=22)
        comparison_result = creation_time < current_time_minus_22_hours
        
        if comparison_result:
            stripe_api.cancel_subscription(user_plan[0]['provider_id'])
            delete_user_plan(id=user_plan[0]['_id'])
            
            subscription = stripe_api.create_subscription(
                customer_id=customer_id,
                product_id=plan[0]['product_id'],
                email=request.user['email'],
            )

            user_plan_data = create_user_plan(plan_id=plan_id, user_id=request.user['_id'], provider_id=subscription['subscription_id'], status=subscription['status'])
            
            if not user_plan_data['success']:
                return JsonResponse({'success': False, 'error': 'Failed to create new user plan.'}, status=500)  
            
            client_secret = subscription['client_secret']
            is_trial = subscription['is_trial']
        else:
            subscription = stripe_api.retrieve_subscription(user_plan[0]['provider_id'])
            client_secret = subscription.latest_invoice.payment_intent.client_secret
        
    return JsonResponse({'success': True, 'result': {'client_secret': client_secret, 'is_trial': is_trial}})

@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def confirm_stripe_payment_intent_view(request):
    try:
        data = json.loads(request.body)
        payment_intent_id = data.get('payment_intent_id')
        
        if not payment_intent_id:
            return JsonResponse({'success': False, 'error': 'Invalid or missing payment intent id data'}, status=400)

    except json.JSONDecodeError as e:
        return JsonResponse({'success': False, 'error': "Invalid or missing payment intent id data"}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': "Invalid or missing payment intent id data"}, status=500)
    
    payment_intent = stripe_api.retrieve_payment_intent(payment_intent_id)
    user_plan = get_user_plans(user_id=request.user['_id'])[0]
    customer_id = get_customer(user_id=request.user['_id'])[0]
    if (
        user_plan and
        payment_intent.customer == customer_id['customer_id'] and
        payment_intent.status == 'succeeded'
    ):
        activate_user_plan(user_plan['_id'])
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=404)

@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def cancel_subscription_view(request, pk):
    user_plan = get_user_plan(id=pk)[0]
    
    if user_plan['is_active']:
        subscription = stripe_api.update_subscription_end_period(user_plan['provider_id'], True)
        expires_at = datetime.fromtimestamp(subscription.cancel_at).strftime('%m/%d/%Y, %I:%M:%S %p')
        result = set_expires_at(id=pk, expires_at=expires_at)
        return JsonResponse({'success': True, 'result': result})
        
    return JsonResponse({'success': True})

@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def upgrade_subscription_view(request, pk):
    try:
        data = json.loads(request.body)
        plan_id = data.get('plan_id')
        
        if not plan_id:
            return JsonResponse({'success': False, 'error': 'Invalid or missing plan id data'}, status=400)

    except json.JSONDecodeError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    plan = get_plan_by_id(id=plan_id)
    if not plan:
        return JsonResponse({'success': False, 'error': 'Invalid plan'}, status=400)
    
    user_plan = get_user_plan(id=pk)[0]
    
    if user_plan['plan_id'] != plan[0]['_id']:
        stripe_api.modify_subscription(user_plan['provider_id'], plan[0]['product_id'])
        update_user_plan_plan_id(id=pk, plan_id=plan[0]['_id'])
    else:
        stripe_api.update_subscription_end_period(user_plan['provider_id'], False)
        set_expires_at(id=pk, expires_at="")
        
    return JsonResponse({'success': True})
    