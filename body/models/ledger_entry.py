from django.db import models
from django.db.models import Sum


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

    @property
    def remaining_consumptions(self):
        if self.quantity < 1:
            return 0

        next_refill = (
            self.medicine.ledgerentry_set.filter(when__gt=self.when, quantity__gt=0)
            .order_by("when")
            .first()
        )

        if next_refill:
            consumptions_for_ledger_entry = self.medicine.consumption_set.filter(
                when__gte=self.when, when__lt=next_refill.when
            )
        else:
            consumptions_for_ledger_entry = self.medicine.consumption_set.filter(
                when__gte=self.when
            )

        total_consumption_quantity = (
            consumptions_for_ledger_entry.aggregate(Sum("quantity"))["quantity__sum"]
            or 0
        )
        return self.quantity - total_consumption_quantity

    class Meta:
        ordering = ["-when"]
        db_table = "ledgerentry"
