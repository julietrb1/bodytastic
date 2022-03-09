from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def report_icon(colour="primary", circular=False):
    circular_class = "circular" if circular else None
    return format_html(
        f'<i aria-hidden="true" class="seedling icon {colour} {circular_class}"></i>'
    )


@register.simple_tag
def emotion_icon(colour="primary", circular=False):
    circular_class = "circular" if circular else None
    return format_html(
        f'<i aria-hidden="true" class="hand holding water icon {colour} {circular_class}"></i>'
    )
