from django.shortcuts import render
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from authentication.decorator import require_auth
from django.http import JsonResponse
from requests.adapters import HTTPAdapter
from django.utils import timezone
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
from updatedai.utils import upload_image
logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(['POST'])
def generate_profile_image_from_text(request):
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt')
        if not prompt:
            return JsonResponse({'success': False, 'message': 'The prompt field is required and cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        width = data.get('width', '512')
        height = data.get('height', '512')
        image_count = data.get('image_count', '1')

        # if not prompt:
        #     return JsonResponse({'success': False, 'message': 'The prompt field is required and cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://stablediffusionapi.com/api/v3/text2img"
        headers = {'Content-Type': 'application/json'}

        payload = json.dumps({
            "key": settings.STABLE_DIFUSSION_API_KEY,
            "model_id": "epicrealism-v3-updat",
            "prompt": prompt,
            "negative_prompt": "painting, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, skinny, glitchy, double torso, extra arms, extra hands, mangled fingers, missing lips, ugly face, distorted face, extra legs, anime",
            "width": width,
            "height": height,
            "samples": image_count,
            "num_inference_steps": 20,
            "seed": None,
            "guidance_scale": 7.5,
            "safety_checker": "yes",
            "multi_lingual": "no",
            "panorama": "no",
            "self_attention": "no",
            "upscale": "no",
            "embeddings_model": None,
            "webhook": None,
            "track_id": None
        })
        response = requests.request("POST", url, headers=headers, data=payload)
        response_data = response.json()
        # return JsonResponse({'results': response_data})
        if response.status_code == 200 and response_data.get('status') == "success":
            print('response_data', response_data)
            # return JsonResponse({'results': 'results'})
            results = []
            time.sleep(4)
            for url in response_data['output']:
                data = upload_image(url)
                if data.get('success'):
                    results.append({'success': True, 'file_url': data.get('file_url')})
                else:
                    results.append({'success': False, 'message': data.get('message', 'Upload failed without error message.')})
            
            return JsonResponse({'results': results})
        else:
            error_message = response_data.get('message', 'Image creation failed.')
            return JsonResponse({'success': False, 'message': error_message}, status=500)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'success': False, 'message': 'API request failed: {}'.format(str(e))}, status=500)
    except KeyError as e:
        return JsonResponse({'success': False, 'message': f'Missing field: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'}, status=500)
