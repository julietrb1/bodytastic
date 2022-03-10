"""Models for the Mind and Soul app of Bodytastic."""

from django.conf import settings
from django.db import models
from django.urls import reverse_lazy


class EmotionReport(models.Model):
    """Instance of a report from a user about how they feel at any given time."""

    when = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notes = models.CharField(max_length=200, blank=True)
    energy_level = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "emotionreport"

    def get_absolute_url(self):
        return reverse_lazy("mind_and_soul:report-detail", kwargs={"pk": self.pk})


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


class EmotionEntry(models.Model):
    """Part of an emotion report from a user, pertaining to a specific emotion."""

    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    report = models.ForeignKey(EmotionReport, on_delete=models.CASCADE)
    strength = models.PositiveSmallIntegerField()
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = "emotionentry"
