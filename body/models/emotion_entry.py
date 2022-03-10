from django.apps import apps

from django.db import models


class EmotionEntry(models.Model):
    """Part of an emotion report from a user, pertaining to a specific emotion."""

    emotion = models.ForeignKey("Emotion", on_delete=models.CASCADE)
    report = models.ForeignKey("EmotionReport", on_delete=models.CASCADE)
    strength = models.PositiveSmallIntegerField()
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = "emotionentry"
