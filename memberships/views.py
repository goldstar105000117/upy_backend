from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from authentication.decorator import require_auth
# from .service import 
import json
import re
from .convex import get_plans

@csrf_exempt
@require_http_methods(["POST"])
# @require_auth
def get_plans_view(request):
    result = get_plans()
    
    if not result:
        return JsonResponse({'success': False, 'error': 'Failed to get plan data'}, status=500)  

    return JsonResponse({'success': True, 'result': result})