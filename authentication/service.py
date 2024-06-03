from twilio.rest import Client
from django.conf import settings

def _get_twilio_verify_client():
    return Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN).verify.services(settings.TWILIO_SERVICE_SID)

def _get_twilio_client():
    return Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)