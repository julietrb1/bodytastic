from django.db import models

from django.apps import apps


class Consumption(models.Model):
    """An instance of consumption of a given medicine by the user."""

    medicine = models.ForeignKey("Medicine", on_delete=models.CASCADE)
    when = models.DateTimeField()
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["-when"]
        db_table = "consumption"

    def __str__(self) -> str:
        return f"({self.quantity}x) {self.when}"
