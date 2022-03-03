from django.contrib import admin

from life_events.models import LifeEvent

@admin.register(LifeEvent)
class LifeEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'when')
