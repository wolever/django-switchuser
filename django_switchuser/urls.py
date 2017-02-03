from django.conf.urls import url
try:
    from django.conf.urls import patterns
except ImportError:
    patterns = lambda _, *p: p

from . import views

urlpatterns = patterns("", *[
    url(r"^$", views.su_login, name="su-login"),
    url(r"^logout$", views.su_logout, name="su-logout"),
])
