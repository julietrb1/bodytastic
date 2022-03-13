from django.apps import apps
from django.utils.timezone import localtime, timedelta
from django.db import models


class Entry(models.Model):
    """A specific body area check-in by a user, describing how it feels, looks, or measures."""

    report = models.ForeignKey("Report", on_delete=models.CASCADE)
    body_area = models.ForeignKey("BodyArea", on_delete=models.CASCADE)
    measurement = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True
    )
    sensations = models.ManyToManyField("Sensation", blank=True)
    notes = models.CharField(max_length=500, blank=True)

    class Meta:
        unique_together = [["report", "body_area"]]
        ordering = ["body_area"]
        db_table = "entry"

    def __str__(self):
        return f"{self.body_area} report"

    @property
    def measurement_with_unit(self):
        return (
            f"{float(self.measurement):g} {self.body_area.measurement_unit}"
            if self.measurement
            else "no measurement"
        )

    @property
    def diff_from_last(self, max_days=14):
        last_entry = (
            Entry.objects.filter(
                report__when__gte=self.report.when - timedelta(days=max_days),
                report__when__lt=self.report.when,
            )
            .order_by("report__when")
            .last()
        )
        if not (last_entry and last_entry.measurement):
            return None

        return self.measurement - last_entry.measurement
