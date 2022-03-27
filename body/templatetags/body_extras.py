from django import template
from django.utils.html import format_html
from django.templatetags.static import static

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


def icons8_image(image_name, width=50):
    return format_html(
        f'<img class="ui image" style="width: {width}px;" src="{static(f"body/icons/icons8-{image_name}")}"/>'
    )


@register.simple_tag
def report_icon(**kwargs):
    return icons8_image("scales-100.png", **kwargs)


@register.simple_tag
def emotion_report_icon(**kwargs):
    return icons8_image("spa-candle-100.png", **kwargs)


@register.simple_tag
def entry_icon(**kwargs):
    return icons8_image("sewing-tape-measure-100.png", **kwargs)


@register.simple_tag
def delete_icon(**kwargs):
    return icons8_image("remove-100.png", **kwargs)


@register.simple_tag
def consumption_icon(**kwargs):
    return icons8_image("treatment-100.png", **kwargs)


@register.simple_tag
def schedule_icon(**kwargs):
    return icons8_image("schedule-100.png", **kwargs)


@register.simple_tag
def emotion_icon(**kwargs):
    return icons8_image("trust-100.png", **kwargs)


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
def medicine_icon(**kwargs):
    return icons8_image("pills-100.png", **kwargs)


@register.simple_tag
def event_icon(**kwargs):
    return icons8_image("prize-100.png", **kwargs)


@register.simple_tag
def home_icon(**kwargs):
    return icons8_image("female-user.svg", **kwargs)


@register.simple_tag
def refill_icon(**kwargs):
    return icons8_image("bill-100.png", **kwargs)
