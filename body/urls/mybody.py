from django.urls import path

import body.views.body as views

ENTRY_CREATE_ROUTE = "entry-create"
ENTRY_DELETE_ROUTE = "entry-delete"
ENTRY_MASS_UPDATE_ROUTE = "entry-mass-update"
ENTRY_UPDATE_ROUTE = "entry-update"
REPORT_CREATE_ROUTE = "report-create"
REPORT_DELETE_ROUTE = "report-delete"
REPORT_DETAIL_ROUTE = "report-detail"
REPORT_LIST_ROUTE = "report-index"
REPORT_UPDATE_ROUTE = "report-update"

urlpatterns = [
    path(
        "",
        views.ReportListView.as_view(),
        name=REPORT_LIST_ROUTE,
    ),
    path(
        "<int:pk>/",
        views.ReportDetailView.as_view(),
        name=REPORT_DETAIL_ROUTE,
    ),
    path(
        "create/",
        views.ReportCreateView.as_view(),
        name=REPORT_CREATE_ROUTE,
    ),
    path(
        "<int:pk>/update/",
        views.ReportUpdateView.as_view(),
        name=REPORT_UPDATE_ROUTE,
    ),
    path(
        "<int:pk>/delete/",
        views.ReportDeleteView.as_view(),
        name=REPORT_DELETE_ROUTE,
    ),
    path(
        "<int:reportpk>/create/",
        views.EntryCreateView.as_view(),
        name=ENTRY_CREATE_ROUTE,
    ),
    path(
        "<int:reportpk>/entries/<int:pk>/update/",
        views.EntryUpdateView.as_view(),
        name=ENTRY_UPDATE_ROUTE,
    ),
    path(
        "<int:reportpk>/entries/mass-update/",
        views.EntryFormView.as_view(),
        name=ENTRY_MASS_UPDATE_ROUTE,
    ),
    path(
        "<int:reportpk>/entries/<int:pk>/delete/",
        views.EntryDeleteView.as_view(),
        name=ENTRY_DELETE_ROUTE,
    ),
]
