from django.views.generic import TemplateView
from django.utils import timezone


class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        now = timezone.localtime()
        if now.hour >= 0 and now.hour <= 5:
            greeting_date_part = "Burning the Midnight Oil"
        elif now.hour >= 6 and now.hour <= 10:
            greeting_date_part = "Good Morning"
        elif now.hour >= 11 and now.hour <= 14:
            greeting_date_part = "Good Day"
        elif now.hour >= 15 and now.hour <= 17:
            greeting_date_part = "Good Afternoon"
        else:
            greeting_date_part = "Good Evening"

        greeting_name_part = self.request.user.first_name or self.request.user.username

        context = super().get_context_data(**kwargs)
        context["greeting"] = f"{greeting_date_part}, {greeting_name_part}"
        context["items"] = [
            {
                "title": "Medication",
                "body": "Never miss a beat. Keep track of consumption and schedules for your meds.",
                "path": "medicine-index",
            },
            {
                "title": "Body",
                "body": "Measurements matter. Keep track of trends and make notes here.",
                "path": "report-index",
            },
            {
                "title": "Life Events",
                "body": "Significant, small, or otherwise, it's probably worth remembering. Note it down here.",
                "path": "event-index",
            },
            {
                "title": "Mind & Soul",
                "body": "You're loved. Feel that? It's your soul saying thank you. Thank it back here.",
                "path": "emotionreport-index",
            },
        ]
        return context

    template_name = "body/index.html"
