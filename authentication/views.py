from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.base.exceptions import TwilioException
import json
import re
import logging
from datetime import datetime
import random
from .convex import (get_user_by_id, add_or_update_tokens_to_user, create_user, delete_token, get_user_by_email,
    get_user_by_username, get_user_profile_by_phone_number, get_user_profile_by_id, generate_confirm_token_for_email, generate_recreate_confirm_token,
    get_profile_by_email_token, verified_email, get_profile_by_phone_code, verified_phone, get_user_profile_by_user_id, activate_deactivate_user,
    generate_confirm_token, get_token_by_token, update_user_password, generate_confirm_token, get_tokens_by_token_and_type_and_userId, delete_token_by_id)
from .decorator import require_auth
from .service import _get_twilio_verify_client, _get_twilio_client
logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def signup_view(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')
        phone_number = data.get('phone_number')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        password = make_password(data.get('password'))

        if not re.match(r"^\S+@\S+\.\S+$", email):
            return JsonResponse({'success': False, 'message': 'Invalid email format.'}, status=400)
        
        if phone_number == None or not re.match(r"^\+?\d{10,15}$", phone_number):
            return JsonResponse({'success': False, 'message': 'Invalid phone number format.'}, status=400)
            
        res = ""
        if email:
            res = get_user_by_email(email)
            if res:
                return JsonResponse({'success': False, 'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if username:
            res = get_user_by_username(username)
            if res:
                return JsonResponse({'success': False, 'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if phone_number:
            res = get_user_profile_by_phone_number(phone_number)
            if res:
                return JsonResponse({'success': False, 'message': 'Phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
        user = create_user(email, password, username, first_name, last_name)
        if user:
            date = timezone.now() + timezone.timedelta(days=1)
            email_expire_at = date.strftime('%m/%d/%Y, %I:%M:%S %p')
            generateConfirmToken = get_random_string(length=16)
            
            profile_data = {
                'confirmation_email_token': str(generateConfirmToken),
                'phone_number': phone_number,
                'email_expire_at': email_expire_at,
                'user_id': user,
            }
            profile_response = generate_confirm_token_for_email(profile_data)
            if not profile_response:
                return JsonResponse({'success': False, 'message': "something wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            verify = _get_twilio_verify_client()
            try:
                verify.verifications.create(channel_configuration={
                    'template_id': settings.EMAIL_CONFIRM_EMIL_TEMPLATE_ID,
                    'from': settings.EMAIL_FROM,
                    'from_name': settings.EMAIL_FROM_NAME,
                    'substitutions': {
                        'token': f'{str(generateConfirmToken)}__{profile_response}'
                    }
                }, to=email, channel='email')
                response = {'success': True, 'message': 'Your account has been created successfully. Please check your email to confirm your email address in order to activate your account.'}
                return JsonResponse(response)
            except TwilioException as e:
                logging.error(e)
                return JsonResponse({'success': False, 'message': 'Failed to send verification email.'}, status=500)
        else:
            return JsonResponse({'message': 'Failed to create user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        return JsonResponse({'success': False, 'message': f'Missing field: {e}'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_http_methods(["POST"])
def signin_view(request):
    
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    user = ""
    try:
        validate_email(username)
        user = get_user_by_email(username)
    except ValidationError:
        user = get_user_by_username(username)
        
    if user and check_password(password, user['password']):
        refresh = RefreshToken()
        refresh['user_id'] = user['_id']
        refresh['email'] = user['email']
        refresh['username'] = user['username']
        str_refresh_token = str(refresh)
        str_access_token = str(refresh.access_token)
        result = add_or_update_tokens_to_user(user, str_access_token, str_refresh_token)
        if result:
            return JsonResponse({
                'access_token': str_access_token,
                'refresh_token': str_refresh_token,
            })
        else:
            return JsonResponse({'message': 'something wrong', "success": False}, status=401)
    return JsonResponse({'message': 'Invalid credentials', "success": False}, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def signout_view(request):
    user = delete_token(request.user)
    if user:
        return JsonResponse({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'Failed to log out'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def refresh_token_view(request):
    old_refresh_token = request.data.get('refresh_token')
    new_refresh_token = RefreshToken(old_refresh_token)
    str_refresh_token = str(new_refresh_token)
    str_access_token = str(new_refresh_token.access_token)
    result = add_or_update_tokens_to_user(request.user, str_access_token, str_refresh_token)
    if result:
        return JsonResponse({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'Failed to log out'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_http_methods(["POST"])
def confirm_email_view(request):
    try:
        data = json.loads(request.body)
        token = data['token']
        id = data['id']
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'message': 'Invalid request. Please provide token Or id.'}, status=400)
    
    try:
        profile_data = {
            'id': id,
            'token': token
        }
        user_profile = get_profile_by_email_token(profile_data)
        if len(user_profile):
            email_confirmed = user_profile[0]['email_confirmed']
            if email_confirmed and user_profile[0]['phone_confirmed']:
                response_data = {
                    'success': False,
                    'message': 'User already verified email and phone number',
                    'code': "completed"
                }
                response = JsonResponse(response_data, status=200)
                return response
            if email_confirmed and user_profile[0]['confirmation_phone_code']:
                return JsonResponse({'success': True, 'message': 'Email Verification is already completed!'}, status=200)

            expired_at_naive = datetime.strptime(user_profile[0]['email_expire_at'], "%m/%d/%Y, %I:%M:%S %p")
            expired_at = timezone.make_aware(expired_at_naive, timezone.get_default_timezone())
            if timezone.now() > expired_at and not email_confirmed:
                response_data = {
                    'success': False,
                    'message': 'The token has been expired.',
                    'code': "expired"
                }
                response = JsonResponse(response_data, status=200)
                return response
            
            
            random_number = random.randint(0, 999999)
            confirmation_phone_code = f"{random_number:06d}"
            date = timezone.now() + timezone.timedelta(days=1)
            phone_expire_at = date.strftime('%m/%d/%Y, %I:%M:%S %p')
            profile_data = {
                'confirmation_phone_code': confirmation_phone_code,
                'phone_expire_at': phone_expire_at,
                'id': user_profile[0]['_id']
            }
            response = verified_email(profile_data)
            if not response:
                return JsonResponse({'success': False, 'result': response['result']}, status=400)

            phone_client = _get_twilio_client()
            message = phone_client.messages.create(
                messaging_service_sid=settings.MESSAGING_SERVICE_SID,
                body=f"{confirmation_phone_code} is your Updated verification code.",
                to='+35795572777'
            )
            print(message)
            if not message.sid:
                return JsonResponse({'success': False, 'message': 'Failed to send verification code via sms.'}, status=500)
            return JsonResponse({'success': True, 'message': 'Email Verification is completed!'}, status=200)
        else:
            return JsonResponse({'success': False, 'message': "Invalid token!"}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': f"The ID is invalid"}, status=400)
    
    
@csrf_exempt
@require_http_methods(["POST"])
def confirm_phone_view(request):
    try:
        data = json.loads(request.body)
        token = data['token']
        id = data['id']
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'message': 'Invalid request. Please provide token.'}, status=400)

    try:
        profile_data = {
            'confirmation_phone_code': token,
            'id': id,
        }
        user_profile = get_profile_by_phone_code(profile_data)
        print('user_profile', user_profile)
        if len(user_profile):
            profile_data = {
                'id': user_profile[0]['_id']
            }

            response = verified_phone(profile_data)
            if not response:
                return JsonResponse({'success': False}, status=500)
            
            profile = get_user_profile_by_id(id)
            user = get_user_by_id(profile['user_id'])
            print('response', response)
            if not response:
                return JsonResponse({'success': False}, status=500)
            
            refresh = RefreshToken()
            refresh['user_id'] = user['_id']
            refresh['email'] = user['email']
            refresh['username'] = user['username']
            str_refresh_token = str(refresh)
            str_access_token = str(refresh.access_token)
            result = add_or_update_tokens_to_user(user, str_access_token, str_refresh_token)        
            
            response_data = {
                'success': True,
                'message': 'Phone Verification is completed!',
                'access_token': str_access_token,
                'refresh_token': str_refresh_token
            }
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({'success': False, 'message': "Invalid token!"}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': f"The ID is invalid"}, status=400)
    
    
@csrf_exempt
@require_http_methods(["POST"])
def resend_email_token_view(request):
    try:
        try:
            data = json.loads(request.body)
            id = data['id']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'success': False, 'message': 'Invalid request. Please provide id.'}, status=400)
        
        try:
            user_profile = get_user_profile_by_id(id)
            if user_profile:
                date = timezone.now() + timezone.timedelta(days=1)
                email_expire_at = date.strftime('%m/%d/%Y, %I:%M:%S %p')
                generateConfirmToken = get_random_string(length=16)
                print('id', user_profile['user_id'])
                profile_data = {
                    'confirmation_email_token': str(generateConfirmToken),
                    'email_expire_at': email_expire_at,
                    'id': id
                }

                response = generate_recreate_confirm_token(profile_data)
                print(response)
                if not response:
                    return JsonResponse({'success': False, 'result': "Something wrong"}, status=201)
                user = get_user_by_id(user_profile['user_id'])
                print('user', user['email'])
                verify = _get_twilio_verify_client()
                try:
                    verify.verifications.create(channel_configuration={
                        'template_id': settings.EMAIL_TEMPLATE_ID,
                        'from': settings.EMAIL_FROM,
                        'from_name': settings.EMAIL_FROM_NAME,
                        'substitutions': {
                            'token': f'{generateConfirmToken}__{id}'
                        }
                    }, to=user['email'], channel='email')
                    response = {'success': True, 'message': 'Just sent token via email successfully.'}
                    return JsonResponse(response)
                except TwilioException as e:
                    logging.error(e)
                    return JsonResponse({'success': False, 'message': 'Failed to send verification email.'}, status=500)
            else:
                return JsonResponse({'success': False, 'message': "Invalid token!"}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f"The ID is invalid"}, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)
    except KeyError as e:
        return JsonResponse({'success': False, 'message': f'Missing field: {e}'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'}, status=500)
    

@csrf_exempt
@require_http_methods(["POST"])
def resend_phone_code_view(request):
    try:
        try:
            data = json.loads(request.body)
            id = data['id']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'success': False, 'message': 'Invalid request. Please provide id.'}, status=400)
        
        try:
            user_profile = get_user_profile_by_id(id)
            if user_profile:
                random_number = random.randint(0, 999999)
                confirmation_phone_code = f"{random_number:06d}"
                date = timezone.now() + timezone.timedelta(days=1)
                phone_expire_at = date.strftime('%m/%d/%Y, %I:%M:%S %p')
                profile_data = {
                    'confirmation_phone_code': confirmation_phone_code,
                    'phone_expire_at': phone_expire_at,
                    'id': id
                }
                response = verified_email(profile_data)
                if not response:
                    return JsonResponse({'success': False, 'result': 'Something wrong'}, status=400)

                phone_client = _get_twilio_client()
                message = phone_client.messages.create(
                    messaging_service_sid=settings.MESSAGING_SERVICE_SID,
                    body=f"{confirmation_phone_code} is your Updated verification code.",
                    to='+35795572777'
                )
                print(message)
                if not message.sid:
                    return JsonResponse({'success': False, 'message': 'Failed to send verification code via sms.'}, status=500)
                return JsonResponse({'success': True, 'message': 'Just sent token via sms successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f"The ID is invalid"}, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)
    except KeyError as e:
        return JsonResponse({'success': False, 'message': f'Missing field: {e}'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'}, status=500)
    

@csrf_exempt
@require_http_methods(["POST"])
def reset_password_view(request):
    try:
        data = json.loads(request.body)
        email = data['email']
        if not email:
            return JsonResponse({'success': False, 'message': 'Email address is required.'}, status=400)
        
        if not re.match(r"^\S+@\S+\.\S+$", email):
            return JsonResponse({'success': False, 'message': 'Invalid email format.'}, status=400)
    except (KeyError, json.JSONDecodeError) as e:
        return JsonResponse({'success': False, 'message': 'Invalid request. Please provide a valid email address.'}, status=400)
    
    try:
        user = get_user_by_email(email)
        if not user:
            return JsonResponse({'success': False, 'message': 'User not found.'}, status=400)
        
        date = timezone.now() + timezone.timedelta(days=1)
        expire_at = date.strftime('%m/%d/%Y, %I:%M:%S %p')
        generateConfirmToken = get_random_string(length=16)

        tokens_data = {
            'token': str(generateConfirmToken),
            'type': "reset_password",
            'expired_at': expire_at,
            'user_id': user['_id'],
        }
        response = generate_confirm_token(tokens_data)
        if not response:
            return JsonResponse({'success': False, 'message': 'Failed to generate reset password token.'}, status=500)
        
        verify = _get_twilio_verify_client()
        try:
            verify.verifications.create(channel_configuration={
                'template_id': settings.EMAIL_REQUEST_RESET_PASSWORD_TEMPLATE_ID,
                'from': settings.EMAIL_FROM,
                'from_name': settings.EMAIL_FROM_NAME,
                'substitutions': {
                    'token': f'{generateConfirmToken}__{response}'
                }
            }, to=email, channel='email')
            return JsonResponse({'success': True, 'message': 'Password reset email sent.'})
        except TwilioException as e:
            logging.error(e)
            return JsonResponse({'success': False, 'message': 'Failed to send password reset email.'}, status=500)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Something wrong'}, status=500)
    

@csrf_exempt
@require_http_methods(["POST"])
def reset_password_validate_view(request):
    try:
        data = json.loads(request.body)
        token = data['token']
        id = data['id']
        
        if not token:
            return JsonResponse({'success': False, 'message': 'The token is required.'}, status=400)

    except (KeyError, json.JSONDecodeError) as e:
        return JsonResponse({'success': False, 'message': 'Invalid request. Please provide token and Id.'}, status=400)
    
    try:
        tokens_data = {
            'id': id,
            'token': token,
        }
        tokens = get_token_by_token(tokens_data)
        if not tokens:
            return JsonResponse({'success': False, 'message': 'Invalid token.'}, status=400)
        
        expired_at_naive = datetime.strptime(tokens['expired_at'], "%m/%d/%Y, %I:%M:%S %p")
        expired_at = timezone.make_aware(expired_at_naive, timezone.get_default_timezone())
        if timezone.now() > expired_at:
            response_data = {
                'success': False,
                'message': 'The token has been expired.',
                'code': "expired"
            }
            response = JsonResponse(response_data, status=200)
            return response

        # if password exist, it's the endpoint to set the password
        password = data.get('password')
        if password:
            user = get_user_by_id(tokens['user_id'])
            print('test2', user)
            update_user_password(user, make_password(password))
            
            return JsonResponse({'success': True, 'message': 'Password reset successfully.'})
        return JsonResponse({'success': True, 'message': 'Token is valid.'})
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Something wrong'}, status=500)


@csrf_exempt
@require_auth
@require_http_methods(["POST"])
def update_password_view(request):
    try:
        data = json.loads(request.body)
        old_password = data['old_password']
        new_password = data['new_password']
        
        if not new_password:
            return JsonResponse({'success': False, 'message': 'The New Password is required.'}, status=400)
        
        if new_password == old_password:
            return JsonResponse({'success': False, 'message': "Old and new passwords are same."}, status=400)
    except (KeyError, json.JSONDecodeError) as e:
        return JsonResponse({'success': False, 'message': 'Invalid request. Please provide both confirm password and new password.'}, status=400)
    
    try:
        user = get_user_by_id(request.user['_id'])
        if not user:
            return JsonResponse({'success': False, 'message': 'User not found.'}, status=404)
        if not check_password(old_password, user['password']):
            return JsonResponse({'success': False, 'message': 'Old password is incorrect.'}, status=400)
        
        update_user_password(user, make_password(new_password))
        return JsonResponse({'success': True, 'message': 'Password updated successfully.'})
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Something wrong'}, status=500)

@csrf_exempt
@require_http_methods(['POST'])
@require_auth
def request_deactivate_account(request):
    if request.method == 'POST':
        try:
            email = request.user['email']
            profile_data = {
                'user_id': request.user['_id']
            }
            user_profile = get_user_profile_by_user_id(profile_data)

            generated_token = get_random_string(length=16)
            date = timezone.now() + timezone.timedelta(days=1)
            expired_at = date.strftime('%m/%d/%Y, %I:%M:%S %p')
        
            token_data = {
                'user_id': request.user['_id'],
                'type': "delete_account",
                'token': str(generated_token),
                'expired_at': expired_at
            }

            result = generate_confirm_token(token_data)
            verify = _get_twilio_verify_client()

            try:
                result = verify.verifications.create(channel_configuration={
                    'template_id': 'd-7146945da8744169a2c58222027c15ff',
                    'from': 'np@updated.com',
                    'from_name': 'Updated',
                    'substitutions': {
                        'token': token_data['token']
                    }
                }, to=email, channel='email')
                
                phone_verify = _get_twilio_verify_client()
                try:
                    result = phone_verify.verifications.create(to=user_profile['phone_number'], channel='sms')
                    return JsonResponse({'success': True, 'message': 'Verification code sent via SMS and email.'})
                except TwilioException as e:
                    logging.error(e)
                    return JsonResponse({'success': False, 'message': 'Failed to send verification code.'}, status=500)
            except TwilioException as e:
                logging.error(e)
                return JsonResponse({'success': False, 'message': 'Failed to send delete account email.'}, status=500)

        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Something wrong'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def confirm_deactivate_account(request):
    try:
        data = json.loads(request.body)
        phone_code = data['phone_code']
        email_code = data['email_code']

        profile_data = {
            'user_id': request.user.id
        }
        user_profile = get_user_profile_by_user_id(profile_data)
        if not phone_code:
            return JsonResponse({'success': False, 'message': 'The phone verification code is required.'}, status=400)
        if not email_code:
            return JsonResponse({'success': False, 'message': 'The email verification code is required.'}, status=400)
        try:
            token_data = {
                'user_id': request.user.id,
                'token': email_code,
                'type': "delete_account"
            }

            tokens = get_tokens_by_token_and_type_and_userId(token_data)
            if tokens['expired_at'] > timezone.now():
                verify = _get_twilio_verify_client()
                try:
                    result = verify.verification_checks.create(to=user_profile.phone_number, code=phone_code)
                    if result.status == 'approved':
                        row_data = {
                            'id': tokens['_id']
                        }
                        result = delete_token_by_id(row_data)
                        if not result:
                            return JsonResponse({'success': False, 'message': 'Failed to delete token.'})
                        
                        user_data = {
                            'is_active': False,
                            'user_id': request.user['_id']
                        }

                        result = activate_deactivate_user(user_data)
                        if not result:
                            return JsonResponse({'success': False, 'message': 'Failed to deactivate user account.'})

                        return JsonResponse({'success': True, 'message': 'Your account successfully deleted.'})
                    else:
                        return JsonResponse({'success': False, 'message': 'Verification failed. The token is invalid or expired.'}, status=400)
                except TwilioException as e:
                    return JsonResponse({'success': False, 'message': 'Failed to verify the token due to a server error.'}, status=500)
            else:
                return JsonResponse({'success': False, 'message': 'The token has expired.'}, status=400)
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid token!'}, status=400)
    except (KeyError, json.JSONDecodeError) as e:
        return JsonResponse({'success': False, 'message': 'Invalid request. Please provide token.'}, status=400)

@csrf_exempt
@require_http_methods(['POST'])
def request_activate_account(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data['phone_number']
            email = data['email']
            
            if not email:
                return JsonResponse({'success': False, 'message': 'The email address is required.'}, status=400)
            
            if not phone_number:
                return JsonResponse({'success': False, 'message': 'The phone number is required.'}, status=400)
            
            if not re.match(r"^\S+@\S+\.\S+$", email):
                return JsonResponse({'success': False, 'message': 'Invalid email format.'}, status=400)
            
            user = get_user_by_email(email)

            if not user:
                response = {'success': False, 'message': "User doesn't exists. Please try to sign up."}
                return JsonResponse(response)
            
            if not re.match(r"^\+?\d{10,15}$", phone_number):
                return JsonResponse({'success': False, 'message': 'Invalid phone number format.'}, status=400)

            generated_token = get_random_string(length=16)
            date = timezone.now() + timezone.timedelta(days=1)
            expired_at = date.strftime('%m/%d/%Y, %I:%M:%S %p')
        
            token_data = {
                'user_id': user['_id'],
                'type': "active_account",
                'token': str(generated_token),
                'expired_at': expired_at
            }

            result = generate_confirm_token_for_email(token_data)

            verify = _get_twilio_verify_client()

            try:
                result = verify.verifications.create(channel_configuration={
                    'template_id': 'd-e8d32254226540338c2cce7eee6828e7',
                    'from': 'np@updated.com',
                    'from_name': 'Updated',
                    'substitutions': {
                        'token': token_data['token']
                    }
                }, to=email, channel='email')
                
                phone_verify = _get_twilio_verify_client()
                try:
                    result = phone_verify.verifications.create(to=phone_number, channel='sms')
                    return JsonResponse({'success': True, 'message': 'Verification code sent via SMS and email.'})
                except TwilioException as e:
                    logging.error(e)
                    return JsonResponse({'success': False, 'message': 'Failed to send verification code.'}, status=500)
            except TwilioException as e:
                logging.error(e)
                return JsonResponse({'success': False, 'message': 'Failed to send delete account email.'}, status=500)

        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Something wrong'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def confirm_activate_account(request):
    try:
        data = json.loads(request.body)
        phone_code = data['phone_code']
        email_code = data['email_code']
        email = data['email']
        phone_number = data['phone_number']

        if not email:
            return JsonResponse({'success': False, 'message': 'The email address is required.'}, status=400)
        
        if not phone_number:
            return JsonResponse({'success': False, 'message': 'The phone number is required.'}, status=400)
        
        if not re.match(r"^\S+@\S+\.\S+$", email):
            return JsonResponse({'success': False, 'message': 'Invalid email format.'}, status=400)
        
        user = get_user_by_email(email)
        
        if not user:
                response = {'success': False, 'message': "User doesn't exists. Please try to sign up."}
                return JsonResponse(response)
            
        if not re.match(r"^\+?\d{10,15}$", phone_number):
            return JsonResponse({'success': False, 'message': 'Invalid phone number format.'}, status=400)
        
        if not phone_code:
            return JsonResponse({'success': False, 'message': 'The phone verification code is required.'}, status=400)
        if not email_code:
            return JsonResponse({'success': False, 'message': 'The email verification code is required.'}, status=400)
        try:
            token_data = {
                'user_id': user['_id'],
                'token': email_code,
                'type': "active_account"
            }

            tokens = get_tokens_by_token_and_type_and_userId(token_data)

            if tokens['expired_at'] > timezone.now():
                verify = _get_twilio_verify_client()
                try:
                    result = verify.verification_checks.create(to=phone_number, code=phone_code)
                    if result.status == 'approved':
                        row_data = {
                            'id': tokens['_id']
                        }
                        result = delete_token_by_id(row_data)
                        
                        user_data = {
                            'is_active': True,
                            'user_id': user['_id']
                        }

                        result = activate_deactivate_user(user_data)
                        if not result:
                            return JsonResponse({'success': False, 'message': 'Failed to activate user account.'})
                        
                        return JsonResponse({'success': True, 'message': 'Your account successfully activated.'})
                    else:
                        return JsonResponse({'success': False, 'message': 'Verification failed. The token is invalid or expired.'}, status=400)
                except TwilioException as e:
                    return JsonResponse({'success': False, 'message': 'Failed to verify the token due to a server error.'}, status=500)
            else:
                return JsonResponse({'success': False, 'message': 'The token has expired.'}, status=400)
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid token!'}, status=400)
    except (KeyError, json.JSONDecodeError) as e:
        return JsonResponse({'success': False, 'message': 'Invalid request. Please provide token.'}, status=400)
    

