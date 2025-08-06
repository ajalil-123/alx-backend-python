

from datetime import datetime, time
import logging
from django.http import HttpResponseForbidden
from django.http import JsonResponse
import time
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



class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_log = {}

    def __call__(self, request):
        ip = self.get_ip_address(request)
        current_time = time.time()

        if request.method == 'POST' and request.path.startswith('/api/messages'):
            # Clean up old entries
            self.requests_log.setdefault(ip, [])
            self.requests_log[ip] = [
                timestamp for timestamp in self.requests_log[ip]
                if current_time - timestamp < 60  # 60 seconds = 1 minute
            ]

            # Check message count in the last 60 seconds
            if len(self.requests_log[ip]) >= 5:
                return JsonResponse(
                    {"error": "Message limit exceeded. Please wait before sending more messages."},
                    status=429
                )

            # Log the new message
            self.requests_log[ip].append(current_time)

        return self.get_response(request)

    def get_ip_address(self, request):
        """Returns the client’s IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
    



class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Only check if user is authenticated
        if user.is_authenticated:
            # Adjust according to how roles are stored (e.g. user.role)
            user_role = getattr(user, 'role', None)

            # Deny access if user is not admin or moderator
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("403 Forbidden: You do not have permission to access this resource.")
        
        # Allow request to continue
        response = self.get_response(request)
        return response
