def su_state(request):
    return {
        "su_state": getattr(request, "su_state", None),
    }
