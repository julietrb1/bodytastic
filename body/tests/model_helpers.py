from django.utils.timezone import make_aware, datetime, localtime
from body.models import (
    Entry,
    Report,
    BodyArea,
    Medicine,
    LedgerEntry,
    Consumption,
    Schedule,
    EmotionReport,
)


def create_emotion_report(
    user, when=make_aware(datetime(2022, 1, 1)), energy_level=5, notes=""
):
    return EmotionReport.objects.create(
        user=user, when=when, energy_level=energy_level, notes=notes
    )


def create_report(user, when=make_aware(datetime(2022, 1, 1)), weight_in_kg=50.5):
    return Report.objects.create(user=user, when=when, weight_in_kg=weight_in_kg)


def create_entry(report, body_area, measurement=20):
    return Entry.objects.create(
        report=report, body_area=body_area, measurement=measurement
    )


def create_body_area(name="Sample Area", measurement_unit="cm"):
    return BodyArea.objects.create(name=name, measurement_unit=measurement_unit)


def create_medicine(user, name="Test meds", current_balance=0):
    return Medicine.objects.create(
        user=user, name=name, current_balance=current_balance
    )


def create_ledger_entry(medicine, quantity, when=localtime()):
    return LedgerEntry.objects.create(medicine=medicine, quantity=quantity, when=when)


def create_consumption(
    medicine, when=make_aware(datetime(2022, 1, 1, 14, 25)), quantity=1
):
    return Consumption.objects.create(medicine=medicine, when=when, quantity=quantity)


def create_schedule(
    medicine,
    start_date,
    end_date,
    frequency_in_days=1,
    time=make_aware(datetime(2022, 1, 1, 14, 25)).time(),
    quantity=1,
    tolerance_mins=30,
):

    return Schedule.objects.create(
        medicine=medicine,
        start_date=start_date,
        end_date=end_date,
        frequency_in_days=frequency_in_days,
        time=time,
        quantity=quantity,
        tolerance_mins=tolerance_mins,
    )
