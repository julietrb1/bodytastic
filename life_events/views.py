from life_events.models import Event
from django.views.generic.list import ListView


class EventListView(ListView):
    model = Event
