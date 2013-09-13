import logging

from django.contrib.auth import SESSION_KEY as AUTH_SESSION_KEY
from django.contrib.auth.models import User

log = logging.getLogger(__name__)

class SuState(object):
    def __init__(self, request):
        self.request = request
        self._reset()

    def _reset(self):
        self.old_user = None
        self.active_user = None
        current_user = self.request.user
        old_user_id = self.request.session.get("su_auth_user_id", None)
        if old_user_id is not None:
            try:
                self.old_user = User.objects.get(id=old_user_id)
                self.active_user = current_user
            except User.DoesNotExist as e:
                log.warning("invalid su_auth_user_id in session for %r: "
                            "%r (reason: %r)", current_user, old_user_id, e)
                self.request.session.pop("su_auth_user_id", None)
                self.request.session.save()
        self.auth_user = self.old_user or current_user

    def is_active(self):
        return self.active_user is not None

    def can_su(self):
        return self.auth_user.is_superuser

    def available_users(self):
        return User.objects.all().order_by("username")

    def user_long_label(self, user):
        return "%s (%s <%s>)" %(user.username, user.get_full_name(), user.email)

    def user_short_label(self, user):
        return user.username

    def set_su_user_id(self, su_user_id):
        su_user = self.available_users().get(id=su_user_id)
        self.request.session[AUTH_SESSION_KEY] = su_user.id
        if su_user_id != self.auth_user.id:
            self.request.session["su_auth_user_id"] = self.auth_user.id
        else:
            self.request.session.pop("su_auth_user_id", None)
        self.request.session.save()
        self.request.user = su_user
        self._reset()

    def clear_su(self):
        self.set_su_user_id(self.auth_user.id)

