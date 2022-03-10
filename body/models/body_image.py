from django.db import models

from body.models.report import Report


class BodyImage(models.Model):
    """An image of the user's body, attached to a report."""

    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    image = models.ImageField()
    notes = models.CharField(max_length=500, blank=True)

    class Meta:
        db_table = "bodyimage"
