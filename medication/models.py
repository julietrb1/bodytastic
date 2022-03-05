"""Models for the Medication app of Bodytastic."""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.timezone import datetime, timedelta


class Medicine(models.Model):
    """A prescription (or other) medication to be consumed by the user, optionally on a schedule."""

    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("medication:medicine-detail", kwargs={"pk": self.pk})

    @property
    def active_schedules(self):
        today = datetime.today().date()
        return self.schedule_set.filter(start_date__lte=today, end_date__gte=today)


class Consumption(models.Model):
    """An instance of consumption of a given medicine by the user."""

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    when = models.DateTimeField()
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["-when"]

    def __str__(self) -> str:
        return f"({self.quantity}x) {self.when}"


class Schedule(models.Model):
    """A schedule to adhere to for consuming a given medicine for a user."""

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    frequency_in_days = models.PositiveSmallIntegerField()
    time = models.TimeField()
    quantity = models.PositiveSmallIntegerField()
    tolerance_mins = models.PositiveSmallIntegerField(
        verbose_name="Tolerance (mins)", default=30
    )

    class Meta:
        ordering = ["-end_date"]

    @property
    def is_active(self):
        return self.next_consumption is not None

    @property
    def next_consumption(self):
        now = datetime.now()

        if self.start_date >= now.date() or self.end_date <= now.date():
            return None

        consumption_at = datetime(
            now.year, now.month, now.day, self.time.hour, self.time.minute
        )

        if now.time() > self.time:
            consumption_at = consumption_at + timedelta(days=1)

        return consumption_at
