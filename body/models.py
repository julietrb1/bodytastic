"""Models for the Body app of Bodytastic."""

from django.conf import settings
from django.db import models
from django.urls import reverse_lazy


class BodyArea(models.Model):
    """Model for an area of the body to be described in a user report."""

    name = models.CharField(max_length=50)
    measurement_unit = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Sensation(models.Model):
    """Describes a feeling or experience, whether emotional or physiological."""

    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class BodyAreaReport(models.Model):
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

    def __str__(self):
        return f"{self.user} on {self.when}"

    def get_absolute_url(self):
        return reverse_lazy("body:report-detail", kwargs={"pk": self.pk})

    @property
    def weight_display(self):
        if not self.weight_in_kg:
            return "no weight"
        return f"{float(self.weight_in_kg):g} kg"


class BodyAreaEntry(models.Model):
    """A specific body area check-in by a user, describing how it feels, looks, or measures."""

    report = models.ForeignKey(BodyAreaReport, on_delete=models.CASCADE)
    body_area = models.ForeignKey(BodyArea, on_delete=models.CASCADE)
    measurement = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True
    )
    sensations = models.ManyToManyField(Sensation, blank=True)
    notes = models.CharField(max_length=500, blank=True)

    class Meta:
        unique_together = [["report", "body_area"]]
        ordering = ["body_area"]

    def __str__(self):
        return f"{self.body_area} report"

    def measurement_with_unit(self):
        return f"{float(self.measurement):g} {self.body_area.measurement_unit}"


class BodyImage(models.Model):
    """An image of the user's body, attached to a report."""

    report = models.ForeignKey(BodyAreaReport, on_delete=models.CASCADE)
    image = models.ImageField()
    notes = models.CharField(max_length=500, blank=True)
