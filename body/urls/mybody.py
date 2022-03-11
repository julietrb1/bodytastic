from django.urls import path

import body.views.body as views

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
        "create/",
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
        "<int:reportpk>/entries/mass-update/",
        views.EntryFormView.as_view(),
        name="entry-mass-update",
    ),
    path(
        "<int:reportpk>/entries/<int:pk>/delete/",
        views.EntryDeleteView.as_view(),
        name="entry-delete",
    ),
]
