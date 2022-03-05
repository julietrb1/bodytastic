from django import template
from django.utils.html import format_html

register = template.Library()


@register.inclusion_tag("medication/schedule_card.html")
def schedule_card(schedule):
    return {"schedule": schedule}


@register.inclusion_tag("medication/consumption_table.html")
def consumption_table(consumptions):
    return {"consumptions": consumptions}


@register.inclusion_tag("medication/medicine_card.html")
def medicine_card(medicine):
    return {"medicine": medicine}


@register.simple_tag
def medicine_icon(colour="primary", circular=False):
    circular_class = "circular" if circular else None
    return format_html(
        f'<i aria-hidden="true" class="pills icon {colour} {circular_class}"></i>'
    )
