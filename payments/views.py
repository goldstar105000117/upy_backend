from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from authentication.decorator import require_auth
import json
from .convex import save_credit
from memberships import stripe_api
from memberships.convex import get_stripe_customer_from_user_id, create_customer, get_customer

@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def create_stripe_payment_intent_view(request):
    try:
        data = json.loads(request.body)
        amount = data.get('amount')
        
        if not amount:
            return JsonResponse({'success': False, 'error': 'Invalid or missing amount data'}, status=400)

    except json.JSONDecodeError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    stripe_customer = get_stripe_customer_from_user_id(user_id=request.user['_id'])
    
    if not stripe_customer:
        customer = stripe_api.create_customer(email=request.user['email'])
        customer_id = customer.id
        
        customer_data = create_customer(customer_id=customer_id, user_id=request.user['_id'])
        if not customer_data['success']:
            return JsonResponse({'success': False, 'error': 'Failed to create new customer.'}, status=500)  
    else:
        customer_id = stripe_customer[0]['customer_id']
        
    payment_intent = stripe_api.create_payment_intent(
        amount=int(amount * 100),
        customer_id=customer_id,
        email=request.user['email'],
    )
    
    client_secret = payment_intent.client_secret
        
    return JsonResponse({'success': True, 'result': {'client_secret': client_secret}})

@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def confirm_stripe_payment_intent_view(request):
    try:
        data = json.loads(request.body)
        payment_intent_id = data.get('payment_intent_id')
        amount = data.get('amount')
        
        if not payment_intent_id:
            return JsonResponse({'success': False, 'error': 'Invalid or missing payment intent id data'}, status=400)
        
        if not amount:
            return JsonResponse({'success': False, 'error': 'Invalid or missing amount data'}, status=400)

    except json.JSONDecodeError as e:
        return JsonResponse({'success': False, 'error': "Invalid or missing payment intent id data"}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': "Invalid or missing payment intent id data"}, status=500)
    
    payment_intent = stripe_api.retrieve_payment_intent(payment_intent_id)
    customer_id = get_customer(user_id=request.user['_id'])[0]
    if (
        payment_intent.customer == customer_id['customer_id'] and
        payment_intent.status == 'succeeded'
    ):
        save_credit(user_id=request.user['_id'], amount=amount)
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=404)