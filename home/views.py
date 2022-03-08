from django.views.generic import TemplateView


class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = [
            {
                "title": "Medication",
                "body": "Never miss a beat. Keep track of consumption and schedules for your meds.",
                "path": "medication:medicine-index",
            },
            {
                "title": "Body",
                "body": "Measurements matter. Keep track of trends and make notes here.",
                "path": "body:report-index",
            },
            {
                "title": "Life Events",
                "body": "Significant, small, or otherwise, it's probably worth remembering. Note it down here.",
                "path": "life_events:event-index",
            },
        ]
        return context

    template_name = "home/index.html"
