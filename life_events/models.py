from django.conf import settings
from django.db import models

class LifeEvent(models.Model):
    name = models.CharField(max_length=60)
    notes = models.CharField(max_length=500, blank=True)
    when = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    class Meta:
        ordering = ['-when']


    def __str__(self) -> str:
        return self.name
