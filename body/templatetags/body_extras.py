from django import template
from django.utils.html import format_html

register = template.Library()


@register.inclusion_tag("body/report_card.html")
def report_card(report):
    optional_tags = []

    if report.weight_in_kg:
        optional_tags.append(("Weight (kg)", f"{float(report.weight_in_kg):.3g}"))

    bra_size = report.bra_size
    if bra_size:
        optional_tags.append(("Bra", bra_size))

    waist_hip_ratio = report.waist_hip_ratio
    if waist_hip_ratio:
        optional_tags.append(("WHR", f"{float(waist_hip_ratio):.2g}"))

    return {"report": report, "optional_tags": optional_tags}


@register.inclusion_tag("body/entry_card.html")
def entry_card(entry):
    diff = entry.diff_from_last

    if not diff:
        colour = "secondary"
    elif diff > 0:
        colour = "orange"
    else:
        colour = "purple"
    return {"entry": entry, "diff": diff, "colour": colour}


@register.simple_tag
def report_icon(colour="primary"):
    return format_html(f'<i aria-hidden="true" class="weight icon {colour}"></i>')


@register.simple_tag
def emotionreport_icon(colour="primary"):
    return format_html(f'<i aria-hidden="true" class="seedling icon {colour}"></i>')


@register.simple_tag
def emotion_icon(colour="primary"):
    return format_html(
        f'<i aria-hidden="true" class="hand holding water icon {colour}"></i>'
    )


@register.inclusion_tag("body/schedule_card.html")
def schedule_card(schedule):
    return {"schedule": schedule}


@register.inclusion_tag("body/consumption_table.html")
def consumption_table(consumptions):
    return {"consumptions": consumptions}


@register.inclusion_tag("body/refill_table.html")
def refill_table(refills):
    refills_with_percent = refills
    for r in refills_with_percent:
        r.remaining_percent = (r.remaining_consumptions / r.quantity) * 100
    return {"refills": refills_with_percent}


@register.inclusion_tag("body/medicine_card.html")
def medicine_card(medicine):
    return {
        "consumption_count": medicine.consumption_set.count(),
        "active_schedule_count": medicine.active_schedules.count(),
        "medicine": medicine,
    }


@register.simple_tag
def medicine_icon(colour="primary"):
    return format_html(f'<i aria-hidden="true" class="pills icon {colour}"></i>')


@register.simple_tag
def event_icon(colour="primary"):
    return format_html(f'<i aria-hidden="true" class="medal icon {colour}"></i>')
