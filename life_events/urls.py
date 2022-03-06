from django.urls import path

from . import views

app_name = "life_events"
urlpatterns = [
    path(
        "",
        views.EventListView.as_view(),
        name="event-index",
    ),
]
