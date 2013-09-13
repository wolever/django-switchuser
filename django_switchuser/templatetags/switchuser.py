from django import template
from django.utils.html import escape

register = template.Library()

@register.simple_tag(takes_context=True)
def su_user_long_label(context, user):
    return escape(context["su_state"].user_long_label(user))


@register.simple_tag(takes_context=True)
def su_user_short_label(context, user):
    return escape(context["su_state"].user_short_label(user))
