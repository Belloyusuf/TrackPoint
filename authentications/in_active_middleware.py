# in_active_middleware.py

from django.contrib.auth import logout
from django.conf import settings
from django.utils import timezone

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Get last activity time from session
            last_activity = request.session.get('last_activity')
            current_time = timezone.now()

            # Check if last activity time is available and if it's older than the threshold
            if last_activity and (current_time - last_activity).total_seconds() > settings.INACTIVE_SESSION_TIMEOUT:
                # If inactive for longer than threshold, log out the user
                logout(request)
            else:
                # Update last activity time in session
                request.session['last_activity'] = current_time

        response = self.get_response(request)
        return response
