from django.urls import path

from body.views.life_events import (
    EventListView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
)

EVENT_CREATE_ROUTE = "event-create"
EVENT_DELETE_ROUTE = "event-delete"
EVENT_LIST_ROUTE = "event-index"
EVENT_UPDATE_ROUTE = "event-update"

urlpatterns = [
    path(
        "",
        EventListView.as_view(),
        name=EVENT_LIST_ROUTE,
    ),
    path(
        "create/",
        EventCreateView.as_view(),
        name=EVENT_CREATE_ROUTE,
    ),
    path(
        "<int:pk>/update/",
        EventUpdateView.as_view(),
        name=EVENT_UPDATE_ROUTE,
    ),
    path(
        "<int:pk>/delete/",
        EventDeleteView.as_view(),
        name=EVENT_DELETE_ROUTE,
    ),
]
