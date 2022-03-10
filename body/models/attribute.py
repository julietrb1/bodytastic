from django.conf import settings
from django.db import models


class Attribute(models.Model):
    """An indication of the environment or situation in which a report was taken, which may
    give additional context to trends or anomalies."""

    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        db_table = "attribute"
