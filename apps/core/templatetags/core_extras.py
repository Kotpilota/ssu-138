from django import template

register = template.Library()


@register.filter
def phone_link(phone):
    digits = "".join(c for c in phone if c.isdigit() or c == "+")
    return f"tel:{digits}"
