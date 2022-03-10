from django.db import models


class Emotion(models.Model):
    """An emotion that the user is capable of feeling at any time.
    This is application-wide and not user-specific."""

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ["name"]
        db_table = "emotion"

    def __str__(self) -> str:
        return self.name
