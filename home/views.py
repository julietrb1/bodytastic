from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    """Shows the home page (for authenticated users only)"""

    template_name = "home/index.html"
