from django.contrib import admin

from body.models import BodyArea, Entry, Sensation, Report, Attribute


@admin.register(BodyArea)
class BodyAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("body_area", "report")


admin.site.register(Sensation)
admin.site.register(Report)
admin.site.register(Attribute)
