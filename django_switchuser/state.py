import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import SESSION_KEY as AUTH_SESSION_KEY
from django.contrib.auth import HASH_SESSION_KEY as AUTH_HASH_SESSION_KEY

log = logging.getLogger(__name__)

class SuState(object):
    def __init__(self, request):
        self.request = request
        self._last_old_user_id = object()

    def _get_old_user_id(self):
        try:
            session = self.request.session
        except AttributeError:
            return None
        return session.get("su_auth_user_id", None)

    @property
    def old_user(self):
        old_user_id = self._get_old_user_id()
        if old_user_id is None:
            return None

        if old_user_id != self._last_old_user_id:
            User = get_user_model()
            self._last_old_user_id = old_user_id
            try:
                self._old_user = User.objects.get(id=old_user_id)
            except User.DoesNotExist as e:
                log.warning("invalid su_auth_user_id in session for %r: "
                            "%r (reason: %r)", self.auth_user, old_user_id, e)
                self.request.session.pop("su_auth_user_id", None)
                self.request.session.save()
                self._old_user = None

        return self._old_user

    @property
    def auth_user(self):
        if self._get_old_user_id() is None:
            try:
                return self.request.user
            except AttributeError:
                return AnonymousUser()
        return self.old_user

    @property
    def active_user(self):
        if self._get_old_user_id() is None:
            return None
        try:
            return self.request.user
        except AttributeError:
            return AnonymousUser()

    def is_active(self):
        return self._get_old_user_id() is not None

    def can_su(self):
        return self.auth_user.is_superuser

    def available_users(self):
        return get_user_model().objects.all().order_by("username")

    def user_long_label(self, user):
        return "%s (%s <%s>)" %(user.username, user.get_full_name(), user.email)

    def user_short_label(self, user):
        return user.username

    def set_su_user_id(self, su_user_id):
        """ Switches to user ID ``su_user_id`` if they are one of the users
            returned by ``available_users()``. """
        su_user = self.available_users().get(id=su_user_id)
        self.set_su_user(su_user)

    def set_su_user(self, su_user):
        """ Switches to user ``su_user`` without permissions checks. """
        self.request.session[AUTH_SESSION_KEY] = su_user.id
        self.request.session[AUTH_HASH_SESSION_KEY] = su_user.get_session_auth_hash()
        if su_user.id != self.auth_user.id:
            self.request.session["su_auth_user_id"] = self.auth_user.id
        else:
            self.request.session.pop("su_auth_user_id", None)
        self.request.session.save()
        self.request.user = su_user

    def clear_su(self):
        self.request.session[AUTH_HASH_SESSION_KEY] = self.auth_user.get_session_auth_hash()
        self.set_su_user(self.auth_user)
