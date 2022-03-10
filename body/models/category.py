from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]
        db_table = "category"

    def __str__(self) -> str:
        return self.name
