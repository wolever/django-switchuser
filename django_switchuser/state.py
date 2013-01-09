from django.contrib.auth import SESSION_KEY as AUTH_SESSION_KEY
from django.contrib.auth.models import User

class SuState(object):
    def __init__(self, request):
        self.request = request
        self._reset()

    def _reset(self):
        current_user = self.request.user
        old_user_id = self.request.session.get("su_auth_user_id", None)
        if old_user_id == current_user.id and current_user.id is not None:
            self.old_user = None
            self.active_user = None
        else:
            self.old_user = User.objects.get(id=old_user_id)
            self.active_user = current_user
        self.auth_user = self.old_user or current_user

    def is_active(self):
        return self.active_user is not None

    def can_su(self):
        return self.auth_user.is_superuser

    def available_users(self):
        return User.objects.all()

    def set_su_user_id(self, su_user_id):
        su_user = self.available_users().get(id=su_user_id)
        self.request.session[AUTH_SESSION_KEY] = su_user.id
        self.request.user = su_user
        self._reset()

    def clear_su(self):
        self.set_su_user_id(self.auth_user.id)

