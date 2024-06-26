from convex import ConvexClient
import os
from dotenv import load_dotenv

load_dotenv()

client = ConvexClient(os.environ.get("CONVEX_URL"))

def get_plans():
    return client.query("membership:get")

def create_plan(type , price , billing_period , discount , storage , token ):
    return client.mutation('membership:createPlan', {
        'type': type,
        'price': price,
        'billing_period': billing_period,
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
    
def deactivate_plan(id):
    return client.mutation('membership:deactivatePlan', {
        'id': id
    })