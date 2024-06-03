from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from convex import ConvexClient
from django.conf import settings
import os
from dotenv import load_dotenv

load_dotenv()

client = ConvexClient(os.environ.get("CONVEX_URL"))

#  -------------------- User -------------------

def get_user_by_id(user_id):
    # Query Convex to get the user by ID
    result = client.mutation('user:getById', {'id': user_id})
    if result['success']:
        return result['result']
    return None

def get_user_by_username(username):
    result = client.mutation('user:getUserByUsername', {'username': username})
    if result['success']:
        return result['result']
    return None

def get_user_by_email(email):
    # Query Convex to get the user by email
    result = client.mutation('user:getUserByEmail', {'email': email})
    if result['success']:
        return result['result']
    return None

def create_user(email, password, username, first_name='', last_name=''):
    # Insert a new user into Convex
    result = client.mutation('user:createUser', {
        'email': email,
        'password': password,  # Ensure the password is hashed before storing
        'username': username,
        'first_name': first_name,
        'last_name': last_name
    })
    print('create_user', result)
    if result['success']:
        return result['result']
    return None

def get_token_by_access_token(access_token):
    # Query Convex to get the user by access token
    result = client.mutation('authtoken:getByAccessToken', {'access_token': access_token})
    if result['success']:
        return result['result']
    return None

def add_or_update_tokens_to_user(user, access_token, refresh_token):
    # Check if a token for the user already exists
    result = client.mutation('authtoken:getByUserId', {
        'user_id': user['_id']
    })
    
    if result['success']:
        # Token exists, update it
        update_result = client.mutation('authtoken:updateToken', {
            'id': result['result']['_id'],
            'access_token': access_token,
            'refresh_token': refresh_token,
        })
        if update_result['success']:
            return update_result['result']
        else:
            return None
    else:
        # Token does not exist, create it
        create_result = client.mutation('authtoken:addToken', {
            'user_id': user['_id'],
            'access_token': access_token,
            'refresh_token': refresh_token,
        })
        if create_result['success']:
            return create_result['result']
        else:
            return None

    
def delete_token(user):
    # Delete the access token from the user in Convex
    result = client.mutation('authtoken:deleteTokenByUserId', {
        'user_id': user['_id'],
    })
    if result['success']:
        return result['result']
    else:
        return None
    
def update_user_password(user, password):
    result = client.mutation('user:updateUserPassword', {
        'user_id': user['_id'],
        'password': password,
    })
    if result['success']:
        return result['result']
    else:
        return None
    
#  -------------------- Profile -------------------
    
def get_user_profile_by_phone_number(phone_number):
    result = client.mutation("profile:getByPhoneNumber", {'phone_number': phone_number})
    if result['success']:
        return result['result']
    else:
        return None
    
def generate_confirm_token_for_email(profile_data):
    result = client.mutation("profile:generateConfirmToken", profile_data)
    if result['success']:
        return result['result']
    else:
        return None
    
def get_profile_by_email_token(profile_data):
    result = client.mutation("profile:getByEmailToken", profile_data)
    if result['success']:
        return result['result']
    else:
        return None

def verified_email(profile_data):
    result = client.mutation("profile:verifiedEmail", profile_data)
    if result['success']:
        return result['result']
    else:
        return None
    
def get_profile_by_phone_code(profile_data):
    result = client.mutation("profile:getByPhoneCode", profile_data)
    if result['success']:
        return result['result']
    else:
        return None

def verified_phone(profile_data):
    result = client.mutation("profile:verifiedPhone", profile_data)
    if result['success']:
        return result['result']
    else:
        return None
    
def get_user_profile_by_id(id):
    result = client.mutation("profile:getById", {'id': id})
    return result[0]

def generate_recreate_confirm_token(profile_data):
    result = client.mutation("profile:generateRecreateConfirmToken", profile_data)
    if result['success']:
        return result['result']
    else:
        return None
    

#  -------------------- Token -------------------

    
def generate_confirm_token(profile_data):
    result = client.mutation("tokens:generateConfirmToken", profile_data)
    if result['success']:
        return result['result']
    else:
        return None
    
def get_token_by_token(token_data):
    result = client.mutation("tokens:getByIdAndToken", token_data)
    if result['success']:
        return result['result'][0]
    else:
        return None

def get_user_profile_by_user_id(profile_data):
    result = client.mutation("profile:getByUserId", profile_data)
    if result['success']:
        return result['result']
    else:
        return None
    
def get_tokens_by_token_and_type_and_userId(token_data):
    result = client.mutation("tokens:getByTokenAndTypeAndUserId", token_data)
    if result['success']:
        return result['result']
    else:
        return None

def delete_token_by_id(row_data):
    result = client.mutation("tokens:deleteRowById", row_data)
    if result['success']:
        return result['result']
    else:
        return None
             
def delete_token_by_id(row_data):
    result = client.mutation("tokens:deleteRowById", row_data)
    if result['success']:
        return result['result']
    else:
        return None

def activate_deactivate_user(row_data):
    result = client.mutation("user:activateOrDeactivateUser", row_data)
    if result['success']:
        return result['result']
    else:
        return None

