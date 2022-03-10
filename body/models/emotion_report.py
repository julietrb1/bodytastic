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
        return reverse_lazy("emotionreport-detail", kwargs={"pk": self.pk})
