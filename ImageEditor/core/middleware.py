import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class DebugCsrfMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug(f"Request method: {request.method}")
        logger.debug(f"CSRF Token from request: {request.COOKIES.get('csrftoken')}")
        logger.debug(f"CSRF Token from POST data: {request.POST.get('csrfmiddlewaretoken')}")
        origin = request.META.get('HTTP_ORIGIN', '')
        referer = request.META.get('HTTP_REFERER', '')

        if origin:
            logger.debug(f"Request Origin: {origin}")
        if referer:
            logger.debug(f"Request Referer: {referer}")
            
        # Check if the origin is in the trusted origins list
        if origin and origin not in settings.CSRF_TRUSTED_ORIGINS:
            logger.warning(f"Untrusted origin detected: {origin}")
        
        response = self.get_response(request)
        
        logger.debug(f"Response status code: {response.status_code}")
        
        return response
