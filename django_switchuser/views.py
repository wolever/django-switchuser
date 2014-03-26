import logging
import urlparse

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

log = logging.getLogger(__name__)

def drop_subdomain(host):
    host_parts = host.split(".")
    if len(host_parts) > 2:
        return host_parts[1:]
    return host_parts

def referrer_path(meta, default=None):
    referrer = meta.get("HTTP_REFERER")
    if not referrer:
        return default
    parsed = urlparse.urlsplit(referrer)
    next_domain = drop_subdomain(parsed.netloc)
    cur_domain = drop_subdomain(meta.get("HTTP_HOST", ""))
    if next_domain != cur_domain:
        return default
    return urlparse.urlunsplit(('', '') + parsed[2:])

def guess_next(request, default=None):
    if "next" in request.GET:
        return request.GET["next"]
    if default is not None:
        return default
    return referrer_path(request.META, default="/")

def redirect_next(request, default=None):
    next = guess_next(request, default)
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
        request.session["su_logout_next"] = (
            request.GET.get("su_logout_next") or
            referrer_path(request.META)
        )
        return redirect_next(request)
    return render(request, "su/login.html", {
        "next": guess_next(request),
    })

def su_logout(request):
    check_su(request)
    if request.method == "POST":
        request.su_state.clear_su()
        default_next = request.session.pop("su_logout_next", None)
        return redirect_next(request, default_next)
    return render(request, "su/logout.html", {
        "next": guess_next(request),
    })
