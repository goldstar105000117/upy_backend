from convex import ConvexClient
import os
from dotenv import load_dotenv

load_dotenv()

client = ConvexClient(os.environ.get("CONVEX_URL"))

def save_credit(user_id, amount):
    return client.mutation('payments:saveCredit', {
        'user_id': user_id,
        'amount': amount
    })