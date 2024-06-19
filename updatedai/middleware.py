from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from updatedai.settings import SECRET_KEY
from datetime import datetime
from authentication.convex import get_user_by_id, get_token_by_access_token
import logging
import jwt
from django.http import JsonResponse
from duffel.convex import save_user_activity
from .constants import URL_DESCRIPTIONS

logger = logging.getLogger(__name__)

def validate_jwt(token):
    logging.info(f"Token received for validation: {token}")
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        logging.info(f"Token is valid. Decoded payload: {decoded}")

        # Log the expiration time for debugging
        expiry_timestamp = decoded.get('exp')
        if expiry_timestamp:
            expiry_datetime = datetime.utcfromtimestamp(expiry_timestamp)
            logging.info(f"Token will expire at {expiry_datetime} UTC")

        return True, decoded
    except jwt.ExpiredSignatureError:
        logging.warning("Token has expired")
        return False, "Token has expired"
    except jwt.InvalidTokenError:
        logging.warning("Invalid token")
        return False, "Invalid token"


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Set the necessary COOP header for Google login
        response["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
        response["Cross-Origin-Embedder-Policy"] = "require-corp"
        
        return response


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("Inside JWTAuthenticationMiddleware")
        token = request.headers.get('Authorization')

        request.user = None

        # If there's no token, do nothing
        if not token:
            return

        # Validate the token
        is_valid, decoded_payload = validate_jwt(token)

        if is_valid:
            user_id = decoded_payload.get('user_id')
            try:
                request.auth = decoded_payload
                token_detail = get_token_by_access_token(token)
                if token_detail:
                    request.user = get_user_by_id(user_id)
                    print(f"Authenticated user: {request.user}")
                else:
                    print(f"Unauthenticated user: {user_id}")
            except Exception as e:
                print(f"Unauthenticated user: {e}")
        else:
            print(f"Token validation failed: {decoded_payload}")
    
class SaveUserActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(request, 'resolver_match'):
            if request.user:
                if 'duffel' in request.resolver_match.route:
                    user_id = request.user['_id']
                    description = URL_DESCRIPTIONS.get(request.resolver_match.route)
                    if description:
                        result = save_user_activity(user_id, description)
                        if not result:
                            return JsonResponse({'success': False, 'error': 'Failed to save user activity'}, status=500)
        return None