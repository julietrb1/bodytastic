from django.contrib import admin

from life_events.models import Event, Category


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "when")


admin.site.register(Category)
