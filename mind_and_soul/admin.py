"""Registers models from the Mind and Soul app for the admin site."""

from django.contrib import admin

from mind_and_soul.models import EmotionReport, Emotion, EmotionEntry

admin.site.register(EmotionReport)
admin.site.register(Emotion)
admin.site.register(EmotionEntry)
