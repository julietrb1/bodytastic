from django.views.generic import TemplateView
from django.utils import timezone


class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        now = timezone.localtime()
        hour_pairs = ((0, 5), (6, 10), (11, 14), (15, 17), (18, 23))
        messages = (
            "Burning the Midnight Oil",
            "Good Morning",
            "Good Day",
            "Good Afternoon",
            "Good Evening",
        )
        greeting_name_part = self.request.user.first_name or self.request.user.username
        greeting_date_part = next(
            message
            for hour_pair, message in zip(hour_pairs, messages)
            if now.hour >= hour_pair[0] and now.hour <= hour_pair[1]
        )
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
