from django.urls import path

from . import views

app_name = "mind_and_soul"
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
]
