from django.http import JsonResponse
from functools import wraps

def require_auth(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            if not request.user:
                return JsonResponse({'message': 'Authentication required'}, status=401)
        except AttributeError:
            return JsonResponse({'message': 'Authentication required'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view