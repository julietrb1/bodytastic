from django.contrib import admin

from body.models import BodyArea, BodyAreaEntry, Sensation, BodyAreaReport


@admin.register(BodyArea)
class BodyAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")


@admin.register(BodyAreaEntry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("body_area", "report")


admin.site.register(Sensation)
admin.site.register(BodyAreaReport)
