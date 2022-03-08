from django.urls import path

from . import views

app_name = "medication"
urlpatterns = [
    path("", views.MedicationListView.as_view(), name="medicine-index"),
    path(
        "create/",
        views.MedicationCreateView.as_view(),
        name="medicine-create",
    ),
    path(
        "<int:pk>/",
        views.MedicationDetailView.as_view(),
        name="medicine-detail",
    ),
    path(
        "<int:pk>/edit/",
        views.MedicationUpdateView.as_view(),
        name="medicine-edit",
    ),
    path(
        "<int:pk>/delete/",
        views.MedicationDeleteView.as_view(),
        name="medicine-delete",
    ),
    path(
        "<int:medicinepk>/consumptions/create/",
        views.ConsumptionCreateView.as_view(),
        name="consumption-create",
    ),
    path(
        "<int:medicinepk>/consumptions/<int:pk>/update/",
        views.ConsumptionUpdateView.as_view(),
        name="consumption-edit",
    ),
    path(
        "<int:medicinepk>/consumptions/<int:pk>/delete/",
        views.ConsumptionDeleteView.as_view(),
        name="consumption-delete",
    ),
    path(
        "<int:medicinepk>/schedules/create/",
        views.ScheduleCreateView.as_view(),
        name="schedule-create",
    ),
    path(
        "<int:medicinepk>/schedules/<int:pk>/update",
        views.ScheduleUpdateView.as_view(),
        name="schedule-edit",
    ),
    path(
        "<int:medicinepk>/schedules/<int:pk>/delete/",
        views.ScheduleDeleteView.as_view(),
        name="schedule-delete",
    ),
    path(
        "<int:medicinepk>/refills/create/",
        views.MedicineRefillCreateView.as_view(),
        name="refill-create",
    ),
    path(
        "<int:medicinepk>/refills/<int:pk>/",
        views.MedicineRefillUpdateView.as_view(),
        name="refill-update",
    ),
    path(
        "<int:medicinepk>/refills/<int:pk>/delete/",
        views.MedicineRefillDeleteView.as_view(),
        name="refill-delete",
    ),
]
