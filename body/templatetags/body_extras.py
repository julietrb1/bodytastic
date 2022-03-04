from django import template
from django.utils.html import format_html

register = template.Library()


@register.inclusion_tag("body/report_card.html")
def report_card(report):
    return {"report": report}


@register.inclusion_tag("body/entry_card.html")
def entry_card(entry):
    return {"entry": entry}


@register.simple_tag
def report_icon(colour="primary", circular=False):
    circular_class = "circular" if circular else None
    return format_html(
        f'<i aria-hidden="true" class="weight icon {colour} {circular_class}"></i>'
    )
