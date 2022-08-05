from django.contrib.auth import logout
from django.contrib import messages
import datetime
from django.shortcuts import redirect

import settings


# This class controls the session
class SessionIdleTimeout:
    def process_request(self, request):
        if request.user.is_authenticated():
            current_datetime = datetime.datetime.now()
            if ('last_login' in request.session):
                last = (current_datetime - request.session['last_login']).seconds
                if last > settings.SESSION_IDLE_TIMEOUT:
                    logout(request, "cafe_order/login.html")
            else:
                request.session['last_login'] = current_datetime
        return None