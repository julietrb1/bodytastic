from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from medication.forms import ConsumptionForm

from .models import Medicine, MedicineConsumption, MedicineSchedule


class UserOnlyMixin:
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ChildUserOnlyMixin:
    def get_queryset(self):
        return self.model.objects.filter(medicine__user=self.request.user)


class MedicineSuccessMixin:
    def get_success_url(self) -> str:
        medicine_pk = self.object.medicine.pk
        return reverse_lazy("medication:medicine-detail", kwargs={"pk": medicine_pk})


class MedicineContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medicine = Medicine.objects.get(pk=self.kwargs["medicinepk"])
        context["medicine"] = medicine
        return context


class MedicineFormMixin:
    def form_valid(self, form):
        medicine = Medicine.objects.get(pk=self.kwargs["medicinepk"])
        form.instance.medicine = medicine
        return super().form_valid(form)


class MedicationListView(UserOnlyMixin, ListView):
    model = Medicine


class MedicationDetailView(UserOnlyMixin, DetailView):
    model = Medicine

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["consumptions"] = MedicineConsumption.objects.filter(medicine=self.object)
        data["schedules"] = MedicineSchedule.objects.filter(medicine=self.object)
        return data


class MedicationCreateView(UserOnlyMixin, CreateView):
    model = Medicine
    fields = ["name"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MedicationUpdateView(UserOnlyMixin, UpdateView):
    model = Medicine
    fields = ["name"]


class MedicationDeleteView(UserOnlyMixin, DeleteView):
    model = Medicine
    success_url = reverse_lazy("medication:medicine-index")


class ConsumptionCreateView(
    ChildUserOnlyMixin,
    MedicineFormMixin,
    MedicineContextMixin,
    MedicineSuccessMixin,
    CreateView,
):
    model = MedicineConsumption
    form_class = ConsumptionForm

    def get_initial(self):
        initial = super().get_initial()
        initial["quantity"] = 1
        initial["when"] = timezone.now()
        return initial


class ConsumptionUpdateView(
    ChildUserOnlyMixin, MedicineContextMixin, MedicineSuccessMixin, UpdateView
):
    model = MedicineConsumption
    form_class = ConsumptionForm


class ConsumptionDeleteView(ChildUserOnlyMixin, MedicineSuccessMixin, DeleteView):
    model = MedicineConsumption


class ScheduleCreateView(
    ChildUserOnlyMixin,
    MedicineFormMixin,
    MedicineContextMixin,
    MedicineSuccessMixin,
    CreateView,
):
    model = MedicineSchedule
    fields = [
        "start_date",
        "end_date",
        "frequency_in_days",
        "time",
        "quantity",
        "tolerance_mins",
    ]


class ScheduleUpdateView(
    ChildUserOnlyMixin, MedicineContextMixin, MedicineSuccessMixin, UpdateView
):
    model = MedicineSchedule
    fields = [
        "start_date",
        "end_date",
        "frequency_in_days",
        "time",
        "quantity",
        "tolerance_mins",
    ]


class ScheduleDeleteView(ChildUserOnlyMixin, MedicineSuccessMixin, DeleteView):
    model = MedicineSchedule
