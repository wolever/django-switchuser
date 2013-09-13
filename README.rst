django-switchuser
=================

``django-switchuser`` makes it easy for an administrator to switch to
temporarily switch to another account by visiting ``/su``.


Assumptions
-----------

Because ``django-switchuser`` was a quick project, it does make one assumption:

* If a user is not allowed to su, then they will get an HTTP 404 if they try
  to visit ``/su/`` or do anything su-related.

* Any superuser is allowed to switch to any other user. *If this assumption does
  not hold*: you'll need to submit a pull request (hint: take a look at
  ``django_switchuser/state.py``)... Sorry :(

Installation
------------

1. ``pip install django-switchuser``
2. Add a few things to ``settings.py`` (note: the ``SuStateMiddleware`` must
   appear *after* the ``AuthenticationMiddleware``)::

    INSTALLED_APPS = (
        ...
        "django_switchuser",
        ...
    )

    MIDDLEWARE_CLASSES = (
        ...
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django_switchuser.middleware.SuStateMiddleware",
        ...
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        "django_switchuser.context_processors.su_state",
        ...
    )

3. Add an entry to ``urls.py`` (note: you can use whatever URL you'd like;
   ``su/`` is simply convenient)::

    urlpatterns += patterns("",
        ...
        url(r"^su/", include("django_switchuser.urls")),
        ...
    )

4. Start the server and check that everything is working by visiting
   http://localhost:8000/su/ *Note*: an HTTP 404 will be returned if the
   currently logged in user isn't allowed to su (by default, only
   administrators are allowed to su).

5. (Optional) Add an entry to your ``base.html`` template which will show a
   convenient logout button::

    <html>
        <head>...</head>
        <body>
            ...
            {% include "su/statusbar.html" %}
        </body>
    </html>

6. (Optional) Override ``SuState`` so it better suits your application. For
   example, to include fields from a user's profile, you subclass ``SuState``
   like this (see below for more detailed documentation)::

    from django.contrib.auth.models import User
    from django_switchuser.state import SuState as DefaultSuState

    class SuState(DefaultSuState):
        def available_users(self):
            return User.objects.all()\
                .select_related("profile")\
                .order_by("profile__client_id")

        def user_long_label(self, user):
            return "%s (%s)" %(user.get_profile().client_id, user.username)

        def user_short_label(self, user):
            return "%s" %(user.get_profile().client_id, )

   And then add to your ``settings.py`` file::

    SU_STATE_CLASS = 'myapp.su.SuState'


Doing Your Own Thing
====================

Doing your own thing is easy. The ``SuStateMiddleware`` and ``su_state``
context processors add a ``su_state`` attribute to the ``request`` and a
``su_state`` variable to the template rendering context. ``su_state`` is an
instance of ``django_switchuser.state.SuState``, and has the following
attributes:

    ``SuState.is_active()``:
        Returns ``True`` if the current user has been switched.

    ``SuState.auth_user``:
        The original user associated with the request. For example, if the user
        ``admin`` has switched to ``jane``, then ``su_state.auth_user`` will be
        ``admin``.

    ``SuState.active_user``:
        The user which has been switched to, or ``None`` if no user has been
        switched. For example, if the user ``admin`` has switched to ``jane``,
        then ``su_state.active_user`` will be ``admin``.

    ``SuState.can_su()``:
        Returns ``True`` if the current user is allowed to switch.

    ``SuState.available_users()``:
        Returns a ``QuerySet`` of ``User`` of the users which the current user
        is allowed to switch to. It may be useful to override this method to
        ``select_related()`` on the user's profile::
        
            def available_users(self):
                return User.objects.all()\
                    .select_related("profile")\
                    .order_by("profile__client_id")

    ``SuState.user_long_label(user)``:
        Returns the "long" label for the user, used in the list of users. It
        may be useful to override this method so that it includes information
        specific to your application::

            def user_long_label(self, user):
                return "%s (%s)" %(user.get_profile().client_id, user.username)

    ``SuState.user_short_label(user)``:
        Returns the "short" label for the user, used in the status bar and
        other places. It may be useful to override this method so that it
        includes information specific to your application::

            def user_short_label(self, user):
                return "%s" %(user.get_profile().client_id, )

    ``SuState.set_su_user_id(su_user_id)``:
        Switches to the user with id ``su_user_id``.

    ``SuState.clear_su()``:
        Reverts back to the original user.

For example, if you don't like the default switch user bar, you could add your
own to your ``base.html``::

    {% load switchuser %}

    {% if su_state.is_active %}
        <a href="{% url su-logout %}">deactive {% su_user_short_label su.active_user %}</a>
    {% elif su_state.can_su %}
        <a href="{% url su-login %}">switch user</a>
    {% endif %}
