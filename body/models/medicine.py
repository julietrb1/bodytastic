from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models import Sum
from django.apps import apps


class Medicine(models.Model):
    """A prescription (or other) medication to be consumed by the user, optionally on a schedule."""

    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_balance = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["name"]
        db_table = "medicine"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("medicine-detail", kwargs={"pk": self.pk})

    @property
    def refills(self):
        return self.ledgerentry_set.filter(quantity__gte=1)

    @property
    def active_schedules(self):
        return apps.get_model("body.Schedule").objects.active(self)

    def recalculate_balance_from_ledger(self):
        self.current_balance = self.ledgerentry_set.all().aggregate(Sum("quantity"))[
            "quantity__sum"
        ]
        self.save()
