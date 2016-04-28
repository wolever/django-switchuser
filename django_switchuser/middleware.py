import sys

from django.conf import settings as s
from importlib import import_module

class SuStateMiddleware(object):
    su_state_fqcn = getattr(s, "SU_STATE_CLASS", "django_switchuser.state.SuState")
    su_state_module_n, _, su_state_class_n = su_state_fqcn.rpartition(".")
    su_state_module = import_module(su_state_module_n)
    su_state_class = getattr(su_state_module, su_state_class_n)

    def process_request(self, request):
        try:
            request.su_state = self.su_state_class(request)
        except AttributeError as e:
            if not hasattr(request, "user"):
                raise AttributeError(
                    str(e) + " (NOTE: django_switchuser must be **after** "
                    "django.contrib.auth.middleware.AuthenticationMiddleware!)"
                ), None, sys.exc_info()[2]
            raise
