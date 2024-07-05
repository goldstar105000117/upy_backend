from convex import ConvexClient
import os
from dotenv import load_dotenv

load_dotenv()

client = ConvexClient(os.environ.get("CONVEX_URL"))

def get_plans():
    return client.query("membership:get")

def create_plan(type, price, billing_period, discount, storage, token, product_id):
    return client.mutation('membership:createPlan', {
        'type': type,
        'price': price,
        'billing_period': billing_period,
        'product_id': product_id,
        'discount': discount,
        'storage': storage,
        'token': token
    })

def update_plan(id, type , price , billing_period , discount , storage , token ):
    return client.mutation('membership:updatePlan', {
        'id': id,
        'type': type,
        'price': price,
        'billing_period': billing_period,
        'discount': discount,
        'storage': storage,
        'token': token
    })
    
def activate_plan(id):
    return client.mutation('membership:activatePlan', {
        'id': id
    })
    
def activate_user_plan(id):
    return client.mutation('membership:activateUserPlan', {
        'id': id
    })
    
def delete_user_plan(id):
    return client.mutation('membership:deleteUserPlan', {
        'id': id
    })
    
def deactivate_plan(id):
    return client.mutation('membership:deactivatePlan', {
        'id': id
    })
    
def get_plan_by_id(id):
    return client.mutation('membership:getById', {
        'id': id
    })
    
def get_user_plan_by_plan_id(plan_id, user_id, complete):
    return client.mutation('membership:getUserPlanByPlanId', {
        'plan_id': plan_id,
        'complete': complete,
        'user_id': user_id
    })

def get_user_plans(user_id):
    return client.mutation('membership:getUserPlans', {
        'user_id': user_id
    })
    
def get_user_plan(id):
    return client.mutation('membership:getUserPlan', {
        'id': id
    })
    
def get_user_plan_by_provider_id(provider_id):
    return client.mutation('membership:getUserPlanByProviderId', {
        'provider_id': provider_id
    })
    
def get_stripe_customer_from_user_id(user_id):
    return client.mutation('membership:getStripeCustomerFromUserId', {
        'user_id': user_id
    })

def create_customer(user_id, customer_id):
    return client.mutation('membership:createCustomer', {
        'user_id': user_id,
        'customer_id': customer_id
    })

def create_user_plan(user_id, plan_id, provider_id, status):
    return client.mutation('membership:createUserPlan', {
        'user_id': user_id,
        'plan_id': plan_id,
        'provider_id': provider_id,
        'status': status
    })

def get_customer(user_id):
    result = client.mutation('membership:getCustomer', {
        'user_id': user_id
    })

    if result:
        return result
    return None

def set_expires_at(id, expires_at):
    return client.mutation('membership:setExpiresAt', {
        'id': id,
        'expires_at': expires_at
    })
    
def update_user_plan_plan_id(id, plan_id):
    return client.mutation('membership:updateUserPlanPlanId', {
        'id': id,
        'plan_id': plan_id
    })
    
def update_user_plan(id, complete, status):
    return client.mutation('membership:updateUserPlan', {
        'id': id,
        'status': status,
        'complete': complete
    })

def get_or_create_user_plan_invoice(invoice_id, provider_id, user_plan_id):
    return client.mutation('membership:getOrCreateUserPlanInvoice', {
        'invoice_id': invoice_id,
        'provider_id': provider_id,
        'user_plan_id': user_plan_id
    })
    
def update_user_plan_invoice(id, status, paid, amount, currency):
    return client.mutation('membership:updateUserPlanInvoice', {
        'id': id,
        'status': status,
        'paid': paid,
        'amount': amount,
        'currency': currency
    })