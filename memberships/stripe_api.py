import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_customer(email):
    return stripe.Customer.create(email=email)

def create_payment_intent(amount, customer_id, user):
    return stripe.PaymentIntent.create(
        customer=customer_id,
        setup_future_usage='off_session',
        amount=amount,
        currency="usd",
        automatic_payment_methods={
            'enabled': True,
        },
        metadata={'email': user.email},
    )

def create_offsession_payment_intent(amount, customer_id, user):
    payment_method = stripe.PaymentMethod.list(customer=customer_id, type="card")
    return stripe.PaymentIntent.create(
        customer=customer_id,
        amount=amount,
        currency="usd",
        automatic_payment_methods={
            'enabled': True,
        },
        payment_method=payment_method.data[0].id,
        off_session=True,
        confirm=True,
        metadata={'email': user.email},
    )

def retrieve_payment_intent(payment_intent_id):
    return stripe.PaymentIntent.retrieve(payment_intent_id)

def cancel_subscription(subscription_id):
    return stripe.Subscription.delete(subscription_id)

def construct_webhook_event(payload, signature):
    endpoint_secret = settings.STRIPE_SIGNING_KEY
    try:
        event = stripe.Webhook.construct_event(
            payload, signature, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e
    data = event['data']['object']
    event_type = event['type']
    result = {}
    
    if 'payment_intent' in event_type and not data.get('invoice'):
        if event_type == 'payment_intent.payment_failed':
            result['type'] = event_type
            result['id'] = data['id']
            result['status'] = data['status']
            result['complete'] = False
        elif event_type == 'payment_intent.succeeded':
            result['type'] = event_type
            result['id'] = data['id']
            result['status'] = data['status']
            result['complete'] = True
    elif event_type == 'invoice.created':
        result['type'] = event_type
        result['id'] = data['subscription']
        result['invoice_id'] = data['id']
        result['paid'] = data['paid']
        result['status'] = data['status']
        result['amount'] = data['amount_due'] / 100
        result['currency'] = data['currency']
    elif event_type == 'invoice.paid':
        result['type'] = event_type
        result['complete'] = True
        result['id'] = data['subscription']
        result['invoice_id'] = data['id']
        result['paid'] = data['paid']
        result['status'] = data['status']
        result['amount'] = data['amount_due'] / 100
        result['currency'] = data['currency']
    elif event_type == 'invoice.payment_action_required':
        result['type'] = event_type
        result['id'] = data['subscription']
        result['invoice_id'] = data['id']
        result['paid'] = data['paid']
        result['status'] = data['status']
        result['amount'] = data['amount_due'] / 100
        result['currency'] = data['currency']
    elif event_type == 'invoice.payment_failed':
        result['type'] = event_type
        result['id'] = data['subscription']
        result['invoice_id'] = data['id']
        result['paid'] = data['paid']
        result['status'] = data['status']
        result['amount'] = data['amount_due'] / 100
        result['currency'] = data['currency']
    elif event_type == 'invoice.updated':
        result['type'] = event_type
        result['id'] = data['subscription']
        result['invoice_id'] = data['id']
        result['paid'] = data['paid']
        result['status'] = data['status']
        result['amount'] = data['amount_due'] / 100
        result['currency'] = data['currency']
    elif event_type == 'customer.subscription.deleted':
        result['type'] = event_type
        result['id'] = data['id']
        result['status'] = data['status']
    elif event_type == 'customer.subscription.created':
        result['complete'] = True if data['status'] in ['active', 'trialing'] else False
        result['type'] = event_type
        result['id'] = data['id']
        result['status'] = data['status']
        result['trial'] = True if data['trial_end'] else False
    elif event_type == 'customer.subscription.updated':
        result['complete'] = True if data['status'] in ['active', 'trialing', 'past_due'] else False
        result['type'] = event_type
        result['id'] = data['id']
        result['status'] = data['status']
        result['expires_at'] = data['cancel_at']
        result['trial'] = True if data['trial_end'] else False
    else:
      print('Unhandled event type {}'.format(event['type']))
      return

    return result

def create_subscription(customer_id, product_id, email):
    customer_id = customer_id
    payment_behavior = {'payment_behavior': 'default_incomplete'}
    payment_settings = {'payment_settings': {'save_default_payment_method': 'on_subscription'}}

    trial_period_days = {}
    is_trial = False
    expand = (
        {'expand': ['latest_invoice.payment_intent']}
    )
    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[
            {
                'price': product_id,
            }
        ],
        **expand,
        **trial_period_days,
        **payment_behavior,
        **payment_settings,
        metadata={'email': email},
    )

    client_secret = (
        subscription.pending_setup_intent.client_secret
        if subscription.pending_setup_intent
        else subscription.latest_invoice.payment_intent.client_secret
    )

    return {
        'subscription_id': subscription.id,
        'client_secret': client_secret,
        'status': subscription.latest_invoice.status,
        'is_trial': is_trial,
    }

def retrieve_subscription(subscription_id):
    return stripe.Subscription.retrieve(subscription_id, expand=['latest_invoice.payment_intent'])

def modify_subscription(subscription_id, plan_provider_id):
    subscription = stripe.Subscription.retrieve(subscription_id)
    stripe.Subscription.modify(
        subscription_id,
        cancel_at_period_end=False,
        proration_behavior='create_prorations',
        items=[{
            'id': subscription['items']['data'][0].id,
            'price': plan_provider_id,
        }]
    )

def update_subscription_end_period(subscription_id, cancel_at_period_end):
    return stripe.Subscription.modify(
        subscription_id,
        cancel_at_period_end=cancel_at_period_end,
    )