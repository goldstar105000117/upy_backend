from twilio.rest import Client
from decouple import config
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.conf import settings
import os
import requests

def _get_twilio_verify_client():
    return Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN).verify.services(settings.TWILIO_SERVICE_SID)

def upload_image(file_link):
    print(file_link)
    filename = os.path.basename(file_link)
    print("Filename:", filename)
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    response1 = requests.get(file_link)
    print(response1)
    if response1.status_code != 200:
        return {"success": True, "file_url": file_link}

    image_data = response1.content
    
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
            return {"success": True, "file_url": f"https://upyai.b-cdn.net/images/{filename}"}
        else:
            return {"success": False, "status_code": response.status_code, "message": response.text}
    except Exception as e:
        return {"success": False, "message": str(e)}
    