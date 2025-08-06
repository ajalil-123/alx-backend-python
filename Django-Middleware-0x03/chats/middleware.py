

from datetime import datetime, time
import logging

from django.http import HttpResponseForbidden



# Create a logger object for this middleware
logger = logging.getLogger('chats.middleware.request_logging')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)
    

# implement a middleware that restricts access to the messaging up during certain hours of the day
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current time
        now = datetime.now().time()

        # Define restricted period: outside 6PM–9PM
        start_allowed = time(18, 0)  # 6:00 PM
        end_allowed = time(21, 0)    # 9:00 PM

        # If current time is outside the allowed window
        if not (start_allowed <= now <= end_allowed):
            return HttpResponseForbidden("Access denied: Chat is only available between 6PM and 9PM.")

        return self.get_response(request)
