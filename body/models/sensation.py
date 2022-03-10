from django.db import models


class Sensation(models.Model):
    """Describes a feeling or experience, whether emotional or physiological."""

    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]
        db_table = "sensation"

    def __str__(self):
        return self.name
