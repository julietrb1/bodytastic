from django.apps import apps

from django.conf import settings
from django.db import models
from django.urls import reverse_lazy


class Report(models.Model):
    """A general body check-in by a user on a given date."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    when = models.DateField()
    weight_in_kg = models.DecimalField(
        verbose_name="Weight (kg)",
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=True,
    )
    attributes = models.ManyToManyField("Attribute", blank=True)

    class Meta:
        ordering = ["-when"]
        unique_together = [["user", "when"]]
        db_table = "report"

    def __str__(self):
        return f"{self.user} on {self.when}"

    def get_absolute_url(self):
        return reverse_lazy("report-detail", kwargs={"pk": self.pk})

    @property
    def weight_display(self):
        if not self.weight_in_kg:
            return "no weight"
        return f"{float(self.weight_in_kg):g} kg"

    @property
    def waist_hip_ratio(self):
        waist_entry = self.entry_set.filter(body_area__name="Waist").first()
        hip_entry = self.entry_set.filter(body_area__name="Hips").first()
        if not waist_entry or not hip_entry:
            return None

        return waist_entry.measurement / hip_entry.measurement
