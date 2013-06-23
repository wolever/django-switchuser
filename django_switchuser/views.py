import logging
import urlparse

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

log = logging.getLogger(__name__)

def guess_next(request):
    if "next" in request.GET:
        return request.GET["next"]
    referer = request.META.get("HTTP_REFERER")
    if not referer:
        return "/"
    parsed = urlparse.urlsplit(referer)
    next = urlparse.urlunsplit(('', '') + parsed[2:])
    return next

def redirect_next(request):
    next = guess_next(request)
    if not next.startswith("/"):
        next = "/" + next
    return HttpResponseRedirect(next)

def check_su(request):
    if not request.su_state.can_su():
        log.warning("user %r isn't allowed to su", request.su_state.auth_user)
        raise Http404

def su_login(request):
    check_su(request)
    if request.method == "POST":
        request.su_state.set_su_user_id(request.POST["user_id"])
        return redirect_next(request)
    return render(request, "su/login.html", {
        "current_user": request.user,
        "next": guess_next(request),
    })

def su_logout(request):
    check_su(request)
    if request.method == "POST":
        request.su_state.clear_su()
        return redirect_next(request)
    return render(request, "su/logout.html", {
        "next": guess_next(request),
    })
