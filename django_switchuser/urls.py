from django.conf.urls import patterns, url

from . import views

patterns = [
    url(r"^$", views.su_login, name="su-login"),
    url(r"^logout$", views.su_logout, name="su-logout"),
]

try:
    urlpatterns = patterns("", *patterns)
except NameError:
    urlpatterns = patterns
