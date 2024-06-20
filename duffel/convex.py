from convex import ConvexClient
import os
from dotenv import load_dotenv

load_dotenv()

client = ConvexClient(os.environ.get("CONVEX_URL"))

def save_user_activity(user_id, action, is_deleted=False):
    result = client.mutation('activity:saveUserActivity', {
        'user_id': user_id,
        'is_deleted': is_deleted,
        'action': action
    })

    if result['success']:
        return result['result']
    return None

def create_new_customer(user_id, customer_id):
    result = client.mutation('customer:createCustomer', {
        'user_id': user_id,
        'customer_id': customer_id
    })

    if result['success']:
        return result['result']
    return None

def get_customer_id(user_id):
    result = client.mutation('customer:getCustomer', {
        'user_id': user_id
    })

    if result:
        return result
    return None