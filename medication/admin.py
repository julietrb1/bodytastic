"""Registers models from the Medication app for the admin site."""

from csv import list_dialects
from django.contrib import admin

from medication.models import Medicine, Consumption, Schedule, LedgerEntry


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "user")


admin.site.register(Consumption)
admin.site.register(Schedule)
admin.site.register(LedgerEntry)
