from django.urls import path

from body.views.body_views import (
    ReportListView,
    ReportDetailView,
    ReportDeleteView,
    ReportCreateView,
    ReportUpdateView,
    EntryDeleteView,
    EntryCreateView,
    EntryUpdateView,
)

urlpatterns = [
    path(
        "",
        ReportListView.as_view(),
        name="report-index",
    ),
    path(
        "<int:pk>/",
        ReportDetailView.as_view(),
        name="report-detail",
    ),
    path(
        "add/",
        ReportCreateView.as_view(),
        name="report-create",
    ),
    path(
        "<int:pk>/update/",
        ReportUpdateView.as_view(),
        name="report-update",
    ),
    path(
        "<int:pk>/delete/",
        ReportDeleteView.as_view(),
        name="report-delete",
    ),
    path(
        "<int:reportpk>/create/",
        EntryCreateView.as_view(),
        name="entry-create",
    ),
    path(
        "<int:reportpk>/entries/<int:pk>/update/",
        EntryUpdateView.as_view(),
        name="entry-update",
    ),
    path(
        "<int:reportpk>/entries/<int:pk>/delete/",
        EntryDeleteView.as_view(),
        name="entry-delete",
    ),
]
