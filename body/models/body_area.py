from django.db import models


class BodyArea(models.Model):
    """Model for an area of the body to be described in a user report."""

    name = models.CharField(max_length=50)
    measurement_unit = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["name"]
        db_table = "bodyarea"

    def __str__(self):
        return self.name
