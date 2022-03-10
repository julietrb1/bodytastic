from django.urls import path

from body.views.life_events import (
    EventListView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
)

urlpatterns = [
    path(
        "",
        EventListView.as_view(),
        name="event-index",
    ),
    path(
        "create/",
        EventCreateView.as_view(),
        name="event-create",
    ),
    path(
        "<int:pk>/update/",
        EventUpdateView.as_view(),
        name="event-update",
    ),
    path(
        "<int:pk>/delete/",
        EventDeleteView.as_view(),
        name="event-delete",
    ),
]
