from django.contrib import admin

from body.models import (
    BodyArea,
    Entry,
    Sensation,
    Report,
    Attribute,
    Event,
    Category,
    EmotionReport,
    Emotion,
    EmotionEntry,
    Medicine,
    Consumption,
    Schedule,
    LedgerEntry,
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "when")


admin.site.register(Category)


@admin.register(BodyArea)
class BodyAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("body_area", "report")


admin.site.register(Sensation)
admin.site.register(Report)
admin.site.register(Attribute)
admin.site.register(EmotionReport)
admin.site.register(Emotion)
admin.site.register(EmotionEntry)


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "user")


admin.site.register(Consumption)
admin.site.register(Schedule)
admin.site.register(LedgerEntry)
