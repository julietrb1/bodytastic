import itertools
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


@register.inclusion_tag("body/schedule_card.html")
def schedule_card(schedule):
    return {"schedule": schedule}


@register.inclusion_tag("body/consumption_table.html")
def consumption_table(consumptions):
    return {"consumptions": consumptions}


@register.inclusion_tag("body/refill_table.html")
def refill_table(refills):
    return {"refills": refills}


@register.inclusion_tag("body/medicine_card.html")
def medicine_card(medicine):
    return {"medicine": medicine}


@register.simple_tag
def medicine_icon(colour="primary", circular=False):
    circular_class = "circular" if circular else None
    return format_html(
        f'<i aria-hidden="true" class="pills icon {colour} {circular_class}"></i>'
    )


@register.simple_tag
def event_icon(colour="primary", circular=False):
    circular_class = "circular" if circular else None
    return format_html(
        f'<i aria-hidden="true" class="medal icon {colour} {circular_class}"></i>'
    )


@register.filter
def chunks(value, chunk_length):
    """
    Breaks a list up into a list of lists of size <chunk_length>
    """
    clen = int(chunk_length)
    i = iter(value)
    while True:
        chunk = list(itertools.islice(i, clen))
        if chunk:
            yield chunk
        else:
            break
