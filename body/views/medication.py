from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from body.forms import ConsumptionForm, RefillForm, ScheduleForm

from body.models import LedgerEntry, Medicine, Consumption, Schedule


class UserOnlyMixin:
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ChildUserOnlyMixin:
    def get_queryset(self):
        return self.model.objects.filter(medicine__user=self.request.user)


class MedicineSuccessMixin:
    def get_success_url(self) -> str:
        medicine_pk = self.object.medicine.pk
        return reverse_lazy("medicine-detail", kwargs={"pk": medicine_pk})


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
        data["schedules_active"] = Schedule.objects.active(self.object)
        data["schedules_future"] = Schedule.objects.future(self.object)
        data["schedules_past"] = Schedule.objects.past(self.object)
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
    success_url = reverse_lazy("medicine-index")


class ConsumptionCreateView(
    ChildUserOnlyMixin,
    MedicineFormMixin,
    MedicineContextMixin,
    MedicineSuccessMixin,
    CreateView,
):
    model = Consumption
    form_class = ConsumptionForm

    def get_initial(self):
        initial = super().get_initial()
        initial["quantity"] = 1
        initial["when"] = timezone.now()
        return initial


class ConsumptionUpdateView(
    ChildUserOnlyMixin, MedicineContextMixin, MedicineSuccessMixin, UpdateView
):
    model = Consumption
    form_class = ConsumptionForm


class ConsumptionDeleteView(ChildUserOnlyMixin, MedicineSuccessMixin, DeleteView):
    model = Consumption


class ScheduleCreateView(
    ChildUserOnlyMixin,
    MedicineFormMixin,
    MedicineContextMixin,
    MedicineSuccessMixin,
    CreateView,
):
    model = Schedule
    form_class = ScheduleForm


class ScheduleUpdateView(
    ChildUserOnlyMixin, MedicineContextMixin, MedicineSuccessMixin, UpdateView
):
    model = Schedule
    form_class = ScheduleForm


class ScheduleDeleteView(ChildUserOnlyMixin, MedicineSuccessMixin, DeleteView):
    model = Schedule


class MedicineRefillCreateView(MedicineSuccessMixin, MedicineFormMixin, CreateView):
    model = LedgerEntry
    template_name = "body/refill_form.html"
    form_class = RefillForm


class MedicineRefillUpdateView(MedicineSuccessMixin, UpdateView):
    model = LedgerEntry
    template_name = "body/refill_form.html"
    form_class = RefillForm


class MedicineRefillDeleteView(MedicineSuccessMixin, DeleteView):
    model = LedgerEntry
    template_name = "body/refill_confirm_delete.html"