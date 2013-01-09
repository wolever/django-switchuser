import sys
from .state import SuState

class SuStateMiddleware(object):
    def process_request(self, request):
        try:
            request.su_state = SuState(request)
        except AttributeError as e:
            if not hasattr(request, "user"):
                raise AttributeError(
                    str(e) + "(NOTE: django_switchuser must be **after** "
                    "django.contrib.auth.middleware.AuthenticationMiddleware!"
                ), None, sys.exc_info()[2]
            raise
