from convex import ConvexClient
import os
from dotenv import load_dotenv

load_dotenv()

client = ConvexClient(os.environ.get("CONVEX_URL"))

def save_user_activity(user_id, action):
    result = client.mutation('activity:saveUserActivity', {
        'user_id': user_id,
        'action': action
    })

    if result['success']:
        return result['result']
    return None