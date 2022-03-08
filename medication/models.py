"""Models for the Medication app of Bodytastic."""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.timezone import datetime, timedelta
from django.db.models import Sum


class Medicine(models.Model):
    """A prescription (or other) medication to be consumed by the user, optionally on a schedule."""

    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_balance = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("medication:medicine-detail", kwargs={"pk": self.pk})

    @property
    def refills(self):
        return self.ledgerentry_set.filter(quantity__gte=1)

    @property
    def active_schedules(self):
        today = datetime.today().date()
        return self.schedule_set.filter(start_date__lte=today, end_date__gte=today)

    def recalculate_balance_from_ledger(self):
        self.current_balance = self.ledgerentry_set.all().aggregate(Sum("quantity"))[
            "quantity__sum"
        ]
        self.save()


class Consumption(models.Model):
    """An instance of consumption of a given medicine by the user."""

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    when = models.DateTimeField()
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["-when"]

    def __str__(self) -> str:
        return f"({self.quantity}x) {self.when}"


class LedgerEntry(models.Model):
    """Helps keep track of how much medication is remaining, and may correspond to consumptions."""

    consumption = models.OneToOneField(
        Consumption, null=True, blank=True, on_delete=models.CASCADE
    )
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    when = models.DateTimeField()
    quantity = models.SmallIntegerField()

    def __str__(self):
        return f"{self.medicine} ({self.quantity})"

    class Meta:
        ordering = ["-when"]


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
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
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

    @property
    def is_active(self):
        now_date = datetime.now().date()
        return self.start_date <= now_date and (
            not self.end_date or self.end_date >= now_date
        )

    @property
    def is_past(self):
        return self.end_date < datetime.now().date()

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
