from django.urls import path

from body.views.mind_and_soul import (
    EmotionReportListView,
    EmotionReportDetailView,
    EmotionReportCreateView,
)

EMOTION_REPORT_CREATE_ROUTE = "emotionreport-create"
EMOTION_REPORT_DETAIL_ROUTE = "emotionreport-detail"
EMOTION_REPORT_LIST_ROUTE = "emotionreport-index"

urlpatterns = [
    path(
        "",
        EmotionReportListView.as_view(),
        name=EMOTION_REPORT_LIST_ROUTE,
    ),
    path(
        "<int:pk>/",
        EmotionReportDetailView.as_view(),
        name=EMOTION_REPORT_DETAIL_ROUTE,
    ),
    path(
        "create/",
        EmotionReportCreateView.as_view(),
        name=EMOTION_REPORT_CREATE_ROUTE,
    ),
]
