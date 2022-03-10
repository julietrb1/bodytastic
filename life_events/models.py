from django.conf import settings
from django.db import models
from django.urls import reverse_lazy


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]
        db_table = "category"

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=60)
    notes = models.CharField(max_length=500, blank=True)
    when = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        ordering = ["-when"]
        db_table = "event"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("life_events:event-index")
