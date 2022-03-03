from django.urls import path

from . import views

app_name = "body"
urlpatterns = [
    path(
        "",
        views.ReportListView.as_view(),
        name="report-index",
    ),
    path(
        "<int:pk>/",
        views.ReportDetailView.as_view(),
        name="report-detail",
    ),
    path(
        "add/",
        views.ReportCreateView.as_view(),
        name="report-create",
    ),
    path(
        "<int:pk>/update/",
        views.ReportUpdateView.as_view(),
        name="report-update",
    ),
    path(
        "<int:pk>/delete/",
        views.ReportDeleteView.as_view(),
        name="report-delete",
    ),
    path(
        "<int:reportpk>/create/",
        views.EntryCreateView.as_view(),
        name="entry-create",
    ),
    path(
        "<int:reportpk>/entries/<int:pk>/update/",
        views.EntryUpdateView.as_view(),
        name="entry-update",
    ),
    path(
        "<int:reportpk>/entries/<int:pk>/delete/",
        views.EntryDeleteView.as_view(),
        name="entry-delete",
    ),
]
