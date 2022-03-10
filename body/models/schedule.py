from django.apps import apps

from django.db import models
from django.utils.timezone import datetime, timedelta


class ScheduleManager(models.Manager):
    def active(self, medicine):
        now_date = datetime.now().date()
        return self.filter(medicine=medicine, start_date__lte=now_date,).exclude(
            end_date__lt=now_date,
        )

    def future(self, medicine):
        now_date = datetime.now().date()
        return self.filter(medicine=medicine, start_date__gt=now_date)

    def past(self, medicine):
        now_date = datetime.now().date()
        return self.filter(medicine=medicine, end_date__lt=now_date)


class Schedule(models.Model):
    """A schedule to adhere to for consuming a given medicine for a user."""

    objects = ScheduleManager()
    medicine = models.ForeignKey("Medicine", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    frequency_in_days = models.PositiveSmallIntegerField(default=1)
    time = models.TimeField()
    quantity = models.PositiveSmallIntegerField(default=1)
    tolerance_mins = models.PositiveSmallIntegerField(
        verbose_name="Tolerance (mins)",
        default=30,
        choices=(
            (5, "5m"),
            (10, "10m"),
            (15, "15m"),
            (20, "20m"),
            (30, "30m"),
            (45, "45m"),
            (60, "1h"),
            (90, "1.5h"),
            (120, "2h"),
        ),
    )

    class Meta:
        ordering = ["-end_date"]
        db_table = "schedule"

    @property
    def is_active(self):
        now_date = datetime.now().date()
        return self.start_date <= now_date and (
            not self.end_date or self.end_date >= now_date
        )

    @property
    def is_past(self):
        return self.end_date and self.end_date < datetime.now().date()

    @property
    def is_future(self):
        return self.start_date > datetime.now().date()

    @property
    def next_consumption(self):
        now = datetime.now()

        consumption_at = datetime(
            now.year, now.month, now.day, self.time.hour, self.time.minute
        )

        if now.time() > self.time:
            consumption_at = consumption_at + timedelta(days=1)

        return consumption_at
