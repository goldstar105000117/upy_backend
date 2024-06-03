from django.shortcuts import render
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from authentication.decorator import require_auth
from django.http import JsonResponse
from requests.adapters import HTTPAdapter
from django.utils import timezone
from .convex import update_profile, insert_interests_tags, deleteInterestsTags, updateInterestsTags, update_user, insertUserInterestsTags, getByPhoneNumber, updateSecurity, updateNotificationSetting, updateEnableNotification, generateConfirmToken, getByTokenAndTypeAndUserId, deleteTokenById, updateUserEmail, insertNewEmail, getNewEmailsByUserId
from authentication.convex import get_user_by_email
from twilio.base.exceptions import TwilioException
from requests.packages.urllib3.util.retry import Retry
from rest_framework import status
from django.conf import settings
from twilio.rest import Client
from django.utils.crypto import get_random_string
import logging
import os
import re
import json
import requests
from datetime import datetime
import random
import time
from updatedai.utils import upload_image, _get_twilio_verify_client
logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def update_profile_data(request):
    try:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        location = request.POST.get('location')
        gender = request.POST.get('gender')
        bio = request.POST.get('bio')
        phone_number = request.POST.get('phone_number')
        birthday = request.POST.get('birthday')
        display_name = request.POST.get('display_name')
        privacy_level = request.POST.get('privacy_level')
        image_url = request.POST.get('image_url')
        image = request.FILES.get('image')

        if not re.match(r"^\+?\d{10,15}$", phone_number):
            return JsonResponse({'success': False, 'message': 'Invalid phone number format. Please provide a valid international phone number.'}, status=status.HTTP_400_BAD_REQUEST)

        phone_number_data = {'phone_number': phone_number}
        phone_data = getByPhoneNumber(phone_number_data)
        if phone_data:
            response = {'success': False, 'message': 'Phone Number already registered.'}
            return JsonResponse(response)
        
    except (KeyError, json.JSONDecodeError) as e:
        print("testtest")
        print("error::::", e)
        return JsonResponse({'success': False, 'message': 'Invalid request. Please provide token.'}, status=status.HTTP_400_BAD_REQUEST)
    
    filename = image.name
    image_data = image.read()
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    REGION = ''
    STORAGE_ZONE_NAME = 'updated-upy'
    ACCESS_KEY = 'f9dfe60e-2b46-457b-ae153a3662eb-293b-4e1e'
    base_url = "storage.bunnycdn.com"
    if REGION:
        base_url = f"{REGION}.{base_url}"

    url = f"https://{base_url}/{STORAGE_ZONE_NAME}/images/{filename}"

    headers = {
        "AccessKey": ACCESS_KEY,
        "Content-Type": "application/octet-stream",
        "accept": "application/json"
    }

    try:
        response = session.put(url, headers=headers, data=image_data)
        if response.status_code == 201:
            file_url = f"https://upyai.b-cdn.net/images/{filename}"
        else:
            return {"success": False, "status_code": response.status_code, "message": response.text}
    except Exception as e:
        return {"success": False, "message": str(e)}

    user = request.user
    last_reset_iso = timezone.now().isoformat()
    
    user_data = {
        'first_name': first_name,
        'last_name': last_name,
        'user_id': user["_id"]
    }
    updated_user_id = update_user(user_data)

    if not updated_user_id:
        return JsonResponse({'message': 'Failed updating user'}, status=status.HTTP_400_BAD_REQUEST)

    avatar = ""
    if image:
        avatar = file_url
    else:
        avatar = image_url

    profile_data = {
        'avatar': avatar,
        'bio': bio,
        'birthday': birthday,
        'display_name': display_name,
        'privacy_level': privacy_level,
        'gender': gender,
        'last_reset': last_reset_iso,
        'location': location,
        'phone_number': phone_number,
        'user_id': user["_id"],
    }

    created_profile_id = update_profile(profile_data)
    # profile_data = client.mutation("profile:get")
    print("Created profile with ID:", created_profile_id)
    
    return JsonResponse({'success': True, 'message': "Profile updated successfully."})

@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def create_interests_tag(request):
    try:
        data = json.loads(request.body)
        name = data.get('name', "")
        interests_tag_data = {
            'name': name,
        }
        response = insert_interests_tags(interests_tag_data)
        if response:
            return JsonResponse({'success': True, 'result': response}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success': False, 'message': response}, status=status.HTTP_400_BAD_REQUEST)

    except json.JSONDecodeError as e:
        return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@require_http_methods(['POST', 'DELETE'])
@require_auth
def update_interests_tag(request, pk):
    try:
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                name = data.get('name', "")
                if not name:
                    return JsonResponse({'success': False, 'message': 'The name field is required and cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)
                
                interests_tag_data = {
                    'name': name,
                    'id': pk,
                }

                response = updateInterestsTags(interests_tag_data)
                if response:
                    return JsonResponse({'success': True, 'result': "Updated InterestsTag successfully"}, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'success': False, 'message': "Failed to update InterestsTag"}, status=status.HTTP_400_BAD_REQUEST)

            except json.JSONDecodeError as e:
                return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=status.HTTP_400_BAD_REQUEST)
            
        elif request.method == 'DELETE':
            # UserInterestsTags.objects.filter(interestsTags__id=pk).delete()
            interests_tag_data = {
                'id': pk,
            }

            response = deleteInterestsTags(interests_tag_data)
            if response:
                return JsonResponse({'success': True, 'result': "Deleted InterestsTag successfully"}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'success': False, 'message': "Failed to delete InterestsTag"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})

@csrf_exempt
@require_http_methods(['POST'])
@require_auth
def insert_interests_tag_user(request):
    try:
        data = json.loads(request.body)
        interests_tag_ids = data.get('interests_tag_ids', "")
        interests_tag_ids_arr = interests_tag_ids.split(",")
        for tag_id in interests_tag_ids_arr:
            tag_data = {
                'id': tag_id,
                'user_id': request.user['_id'],
            }
            response = insertUserInterestsTags(tag_data)
            if not response:
                return JsonResponse({'success': False, 'message': "Failed to add user InterestsTag."})
        if response:
            return JsonResponse({'success': True, 'message': "Added user InterestsTag successfully."})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})
@csrf_exempt
@require_http_methods(['POST'])
@require_auth
def update_security(request):
    try:
        try:
            data = json.loads(request.body)
            auto_approve_friend_request = data.get('auto_approve_friend_request')
            hide_online_status = data.get('hide_online_status')
            visibility = data.get('visibility')
        except ValueError:
            return JsonResponse({'success': False, 'message': "Invalid input for boolean fields."}, status=status.HTTP_400_BAD_REQUEST)

        security_data = {
            'auto_approve_friend_request': int(auto_approve_friend_request),
            'hide_online_status': int(hide_online_status),
            'visibility': visibility,
            'user_id': request.user['_id'],
        }

        response = updateSecurity(security_data)
        if response:
            return JsonResponse({'success': True, 'message': "Security settings updated successfully."}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success': True, 'message': "Failed to update Security settings."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'success': False, "message": str(e)})

@csrf_exempt
@require_http_methods(['POST'])
@require_auth
def update_email_notification_settings(request):
    try:
        try:
            data = json.loads(request.body)
            emailNotificationTypes = data.get('emailNotificationTypes', "")
        except ValueError:
            return JsonResponse({'success': False, 'message': "Invalid input for boolean fields."}, status=status.HTTP_400_BAD_REQUEST)

        notification_data = {
            'notificationRecieveConfig': str(emailNotificationTypes),
            'user_id': request.user['_id'],
        }

        response = updateNotificationSetting(notification_data)
        
        if response:
            return JsonResponse({'success': True, 'message': "Email notification settings updated successfully."}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success': False, 'message': "Failed to update Email notification settings."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def enable_notification(request):
    try:
        enable_notification_data = {
            'enable_notification': True,
            'user_id': request.user['_id'],
        }
        response = updateEnableNotification(enable_notification_data)
        if response:
            return JsonResponse({'success': True, 'message': "Enabled notification successfully."}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success': True, 'message': "Failed to enable notification."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def disable_notification(request):
    try:
        enable_notification_data = {
            'enable_notification': False,
            'user_id': request.user['_id'],
        }
        response = updateEnableNotification(enable_notification_data)
        if response:
            return JsonResponse({'success': True, 'message': "Enabled notification successfully."}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success': True, 'message': "Failed to enable notification."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def request_update_email(request):
    try:
        try:
            data = json.loads(request.body)
            email = data.get('email', "")
            if not email:
                return JsonResponse({'success': False, 'message': 'The email field is required and cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not re.match(r"^\S+@\S+\.\S+$", email):
                return JsonResponse({'success': False, 'message': 'Invalid email format.'}, status=status.HTTP_400_BAD_REQUEST)
            
            isEmailExist = get_user_by_email(email)
            if isEmailExist:
                return JsonResponse({'success': False, 'message': 'Email already registered.'})
        except ValueError:
            return JsonResponse({'success': False, 'message': "Invalid input for boolean fields."}, status=status.HTTP_400_BAD_REQUEST)

        verify = _get_twilio_verify_client()

        date = timezone.now() + timezone.timedelta(days=1)
        expire_at = date.strftime('%m/%d/%Y, %I:%M:%S %p')
        random_number = random.randint(0, 999999)
        confirmation_phone_code = f"{random_number:06d}"
        
        tokens_data = {
            'token': f'{confirmation_phone_code}__{request.user["_id"]}',
            'type': "update_email",
            'expired_at': expire_at,
            'user_id': request.user['_id'],
        }

        response = generateConfirmToken(tokens_data)

        if not response:
            return JsonResponse({'success': False, 'message': "Failed to generate confirm token"}, status=status.HTTP_400_BAD_REQUEST)
        
        new_emails_data = {
            'new_email': email,
            'user_id': request.user['_id'],
        }

        response = insertNewEmail(new_emails_data)

        if not response:
            return JsonResponse({'success': False, 'message': "Failed to generate confirm token"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            result = verify.verifications.create(
                channel_configuration={
                    'template_id': 'd-89dcaf6274e24bfcb1c0a74177c59298',
                    'from': 'np@updated.com',
                    'from_name': 'Updated',
                    'substitutions': {
                        'token': f'{confirmation_phone_code}__{request.user["_id"]}'
                    }
                },
                to=request.user['email'],
                channel='email'
            )
            return JsonResponse({'success': True, 'message': "Send verification code successfully."})
        except TwilioException as e:
            logging.error(e)
            return JsonResponse({'success': False, 'message': 'Failed to send verification email.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def confirm_update_original_email(request):
    try:
        data = json.loads(request.body)
        token = data.get('token', "")

        new_email_data = {
            'user_id': request.user['_id']
        }
        result = getNewEmailsByUserId(new_email_data)

        if not result:
            return JsonResponse({'success': False, 'message': 'New Email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                
        new_email = result['new_email']
        if not new_email:
            return JsonResponse({'success': False, 'message': 'The email field is required and cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not token:
            return JsonResponse({'success': False, 'message': 'The token field is required and cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not re.match(r"^\S+@\S+\.\S+$", new_email):
            return JsonResponse({'success': False, 'message': 'Invalid email format.'}, status=status.HTTP_400_BAD_REQUEST)

        isEmailExist = get_user_by_email(new_email)
        if isEmailExist:
            return JsonResponse({'success': False, 'message': 'Email already registered.'})
    except ValueError:
        return JsonResponse({'success': False, 'message': "Invalid input for boolean fields."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        tokens_data = {
            'token': token,
            'user_id': request.user['_id'],
            'type': "update_email"
        }
        tokens = getByTokenAndTypeAndUserId(tokens_data)

        expired_at_naive = datetime.strptime(tokens['expired_at'], "%m/%d/%Y, %I:%M:%S %p")
        expired_at = timezone.make_aware(expired_at_naive, timezone.get_default_timezone())
        if expired_at > timezone.now():
            tokens_data = {
                'id': tokens['_id']
            }
            response = deleteTokenById(tokens_data)
            if not response:
                return JsonResponse({'success': False, 'message': 'Failed to delete token'}, status=status.HTTP_400_BAD_REQUEST)
            
            verify = _get_twilio_verify_client()

            date = timezone.now() + timezone.timedelta(days=1)
            expire_at = date.strftime('%m/%d/%Y, %I:%M:%S %p')
            random_number = random.randint(0, 999999)
            confirmation_phone_code = f"{random_number:06d}"
            
            tokens_data = {
                'token': f'{confirmation_phone_code}__{request.user["_id"]}',
                'type': "update_email",
                'expired_at': expire_at,
                'user_id': request.user['_id'],
            }

            response = generateConfirmToken(tokens_data)
            if not response:
                return JsonResponse({'success': False, 'message': "Failed to generate confirm token"}, status=status.HTTP_400_BAD_REQUEST)

            result = verify.verifications.create(
                channel_configuration={
                    'template_id': 'd-89dcaf6274e24bfcb1c0a74177c59298',
                    'from': 'np@updated.com',
                    'from_name': 'Updated',
                    'substitutions': {
                        'token': f'{confirmation_phone_code}__{request.user["_id"]}'
                    }
                },
                to=new_email,
                channel='email'
            )
            return JsonResponse({'success': True, 'message': "Send verification code successfully."})

        else:
            return JsonResponse({'success': False, 'message': 'The token has expired.'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def confirm_update_new_email(request):
    try:
        data = json.loads(request.body)
        token = data.get('token', "")
        
        if not token:
            return JsonResponse({'success': False, 'message': 'The token field is required and cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)
        
        new_email_data = {
            'user_id': request.user['_id']
        }
        result = getNewEmailsByUserId(new_email_data)
        new_email = result['new_email']

        if not re.match(r"^\S+@\S+\.\S+$", new_email):
            return JsonResponse({'success': False, 'message': 'Invalid email format.'}, status=status.HTTP_400_BAD_REQUEST)

        isEmailExist = get_user_by_email(new_email)
        if isEmailExist:
            return JsonResponse({'success': False, 'message': 'Email already registered.'})
    except ValueError:
        return JsonResponse({'success': False, 'message': "Invalid input for boolean fields."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        tokens_data = {
            'token': token,
            'user_id': request.user['_id'],
            'type': "update_email"
        }
        tokens = getByTokenAndTypeAndUserId(tokens_data)

        expired_at_naive = datetime.strptime(tokens['expired_at'], "%m/%d/%Y, %I:%M:%S %p")
        expired_at = timezone.make_aware(expired_at_naive, timezone.get_default_timezone())
        if expired_at > timezone.now():
            user_data = {
                'user_id': request.user['_id'],
                'email': new_email
            }
            response = updateUserEmail(user_data)
            if not response:
                return JsonResponse({'success': False, 'message': 'Failed to update user email'}, status=status.HTTP_400_BAD_REQUEST)

            tokens_data = {
                'id': tokens['_id']
            }
            response = deleteTokenById(tokens_data)
            if not response:
                return JsonResponse({'success': False, 'message': 'Failed to delete token'}, status=status.HTTP_400_BAD_REQUEST)
            
            return JsonResponse({'success': True, 'message': "Email updated successfully."})
        else:
            return JsonResponse({'success': False, 'message': 'The token has expired.'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})