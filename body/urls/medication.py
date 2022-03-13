from django.urls import path

from body.views import medication as medication_views

CONSUMPTION_CREATE_ROUTE = "consumption-create"
CONSUMPTION_CREATE_DEFAULT_ROUTE = "consumption-create-default"
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
    path("", medication_views.MedicineListView.as_view(), name=MEDICINE_LIST_ROUTE),
    path(
        "create/",
        medication_views.MedicineCreateView.as_view(),
        name=MEDICINE_CREATE_ROUTE,
    ),
    path(
        "<int:pk>/",
        medication_views.MedicineDetailView.as_view(),
        name=MEDICINE_DETAIL_ROUTE,
    ),
    path(
        "<int:pk>/edit/",
        medication_views.MedicineUpdateView.as_view(),
        name=MEDICINE_UPDATE_ROUTE,
    ),
    path(
        "<int:pk>/delete/",
        medication_views.MedicineDeleteView.as_view(),
        name=MEDICINE_DELETE_ROUTE,
    ),
    path(
        "<int:medicinepk>/consumptions/create/",
        medication_views.ConsumptionCreateView.as_view(),
        name=CONSUMPTION_CREATE_ROUTE,
    ),
    path(
        "<int:medicinepk>/consumptions/create-default/",
        medication_views.ConsumptionCreateDefaultView.as_view(),
        name=CONSUMPTION_CREATE_DEFAULT_ROUTE,
    ),
    path(
        "<int:medicinepk>/consumptions/<int:pk>/update/",
        medication_views.ConsumptionUpdateView.as_view(),
        name=CONSUMPTION_UPDATE_ROUTE,
    ),
    path(
        "<int:medicinepk>/consumptions/<int:pk>/delete/",
        medication_views.ConsumptionDeleteView.as_view(),
        name=CONSUMPTION_DELETE_ROUTE,
    ),
    path(
        "<int:medicinepk>/schedules/create/",
        medication_views.ScheduleCreateView.as_view(),
        name=SCHEDULE_CREATE_ROUTE,
    ),
    path(
        "<int:medicinepk>/schedules/<int:pk>/update/",
        medication_views.ScheduleUpdateView.as_view(),
        name=SCHEDULE_UPDATE_ROUTE,
    ),
    path(
        "<int:medicinepk>/schedules/<int:pk>/delete/",
        medication_views.ScheduleDeleteView.as_view(),
        name=SCHEDULE_DELETE_ROUTE,
    ),
    path(
        "<int:medicinepk>/refills/create/",
        medication_views.MedicineRefillCreateView.as_view(),
        name=REFILL_CREATE_ROUTE,
    ),
    path(
        "<int:medicinepk>/refills/<int:pk>/",
        medication_views.MedicineRefillUpdateView.as_view(),
        name=REFILL_UPDATE_ROUTE,
    ),
    path(
        "<int:medicinepk>/refills/<int:pk>/delete/",
        medication_views.MedicineRefillDeleteView.as_view(),
        name=REFILL_DELETE_ROUTE,
    ),
]
