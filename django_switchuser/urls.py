from django import VERSION
try:
    from django.conf.urls import patterns, url
except:
    from django.conf.urls import url
from . import views

if VERSION > (1, 10):
    urlpatterns = [
        url(r"^$", views.su_login, name="su-login"),
        url(r"^logout$", views.su_logout, name="su-logout"),
    ]

else:
    urlpatterns = patterns("",
        url(r"^$", views.su_login, name="su-login"),
        url(r"^logout$", views.su_logout, name="su-logout"),
    )
