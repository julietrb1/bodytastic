from django import template

register = template.Library()


@register.inclusion_tag("medication/schedule_card.html")
def schedule_card(schedule):
    return {"schedule": schedule}


@register.inclusion_tag("medication/consumption_card.html")
def consumption_card(consumption):
    return {"consumption": consumption}


@register.inclusion_tag("medication/medicine_card.html")
def medicine_card(medicine):
    return {"medicine": medicine}
