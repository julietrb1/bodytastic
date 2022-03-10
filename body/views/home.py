from django.views.generic import TemplateView


class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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