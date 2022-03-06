from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def event_icon(colour="primary", circular=False):
    circular_class = "circular" if circular else None
    return format_html(
        f'<i aria-hidden="true" class="medal icon {colour} {circular_class}"></i>'
    )
