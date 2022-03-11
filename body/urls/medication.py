from django.urls import path

from body.views.medication import (
    MedicineListView,
    MedicineDetailView,
    MedicineCreateView,
    MedicineUpdateView,
    MedicineDeleteView,
    ConsumptionCreateView,
    ConsumptionUpdateView,
    ConsumptionDeleteView,
    ScheduleCreateView,
    ScheduleUpdateView,
    ScheduleDeleteView,
    MedicineRefillCreateView,
    MedicineRefillUpdateView,
    MedicineRefillDeleteView,
)

CONSUMPTION_CREATE_ROUTE = "consumption-create"
CONSUMPTION_DELETE_ROUTE = "consumption-delete"
CONSUMPTION_UPDATE_ROUTE = "consumption-edit"
MEDICINE_CREATE_ROUTE = "medicine-create"
MEDICINE_DELETE_ROUTE = "medicine-delete"
MEDICINE_DETAIL_ROUTE = "medicine-detail"
MEDICINE_LIST_ROUTE = "medicine-index"
MEDICINE_UPDATE_ROUTE = "medicine-edit"
REFILL_CREATE_ROUTE = "refill-create"
REFILL_DELETE_ROUTE = "refill-delete"
REFILL_UPDATE_ROUTE = "refill-update"
SCHEDULE_CREATE_ROUTE = "schedule-create"
SCHEDULE_DELETE_ROUTE = "schedule-delete"
SCHEDULE_UPDATE_ROUTE = "schedule-update"

urlpatterns = [
    path("", MedicineListView.as_view(), name=MEDICINE_LIST_ROUTE),
    path(
        "create/",
        MedicineCreateView.as_view(),
        name=MEDICINE_CREATE_ROUTE,
    ),
    path(
        "<int:pk>/",
        MedicineDetailView.as_view(),
        name=MEDICINE_DETAIL_ROUTE,
    ),
    path(
        "<int:pk>/edit/",
        MedicineUpdateView.as_view(),
        name=MEDICINE_UPDATE_ROUTE,
    ),
    path(
        "<int:pk>/delete/",
        MedicineDeleteView.as_view(),
        name=MEDICINE_DELETE_ROUTE,
    ),
    path(
        "<int:medicinepk>/consumptions/create/",
        ConsumptionCreateView.as_view(),
        name=CONSUMPTION_CREATE_ROUTE,
    ),
    path(
        "<int:medicinepk>/consumptions/<int:pk>/update/",
        ConsumptionUpdateView.as_view(),
        name=CONSUMPTION_UPDATE_ROUTE,
    ),
    path(
        "<int:medicinepk>/consumptions/<int:pk>/delete/",
        ConsumptionDeleteView.as_view(),
        name=CONSUMPTION_DELETE_ROUTE,
    ),
    path(
        "<int:medicinepk>/schedules/create/",
        ScheduleCreateView.as_view(),
        name=SCHEDULE_CREATE_ROUTE,
    ),
    path(
        "<int:medicinepk>/schedules/<int:pk>/update",
        ScheduleUpdateView.as_view(),
        name=SCHEDULE_UPDATE_ROUTE,
    ),
    path(
        "<int:medicinepk>/schedules/<int:pk>/delete/",
        ScheduleDeleteView.as_view(),
        name=SCHEDULE_DELETE_ROUTE,
    ),
    path(
        "<int:medicinepk>/refills/create/",
        MedicineRefillCreateView.as_view(),
        name=REFILL_CREATE_ROUTE,
    ),
    path(
        "<int:medicinepk>/refills/<int:pk>/",
        MedicineRefillUpdateView.as_view(),
        name=REFILL_UPDATE_ROUTE,
    ),
    path(
        "<int:medicinepk>/refills/<int:pk>/delete/",
        MedicineRefillDeleteView.as_view(),
        name=REFILL_DELETE_ROUTE,
    ),
]
