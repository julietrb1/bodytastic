from django.apps import apps

from django.db import models


class LedgerEntry(models.Model):
    """Helps keep track of how much medication is remaining, and may correspond to consumptions."""

    consumption = models.OneToOneField(
        "Consumption",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    medicine = models.ForeignKey("Medicine", on_delete=models.CASCADE)
    when = models.DateTimeField()
    quantity = models.SmallIntegerField()

    def __str__(self):
        return f"{self.medicine} ({self.quantity})"

    class Meta:
        ordering = ["-when"]
        db_table = "ledgerentry"
