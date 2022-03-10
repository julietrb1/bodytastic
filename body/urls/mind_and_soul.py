from django.urls import path

from body.views.mind_and_soul_views import (
    EmotionReportListView,
    EmotionReportDetailView,
    EmotionReportCreateView,
)

urlpatterns = [
    path(
        "",
        EmotionReportListView.as_view(),
        name="emotionreport-index",
    ),
    path(
        "<int:pk>/",
        EmotionReportDetailView.as_view(),
        name="emotionreport-detail",
    ),
    path(
        "create/",
        EmotionReportCreateView.as_view(),
        name="emotionreport-create",
    ),
]
