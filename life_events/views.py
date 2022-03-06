from life_events.forms import EventForm
from life_events.models import Event
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView


class UserOnlyMixin:
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class EventListView(UserOnlyMixin, ListView):
    model = Event


class EventCreateView(UserOnlyMixin, CreateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EventUpdateView(UserOnlyMixin, UpdateView):
    model = Event
    form_class = EventForm


class EventDeleteView(UserOnlyMixin, DeleteView):
    model = Event
