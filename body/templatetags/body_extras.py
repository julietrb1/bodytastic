from django import template

register = template.Library()


@register.inclusion_tag("body/report_card.html")
def report_card(report):
    return {"report": report}


@register.inclusion_tag("body/entry_card.html")
def entry_card(entry):
    return {"entry": entry}
