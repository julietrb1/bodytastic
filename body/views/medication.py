from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import localtime
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages

from body.forms import RefillForm, ScheduleForm
from body.forms.form_mixins import WhenFieldMixin
from body.messages import fui_msg_text

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


class MedicineListView(UserOnlyMixin, ListView):
    model = Medicine

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if self.object_list.count() == 1:
            messages.info(
                self.request,
                fui_msg_text(
                    f"Jumped to Medicine",
                    f"Took a shortcut to the only medicine you have. <a href=\"{reverse('medicine-create')}\">Add one here.</a>",
                ),
            )
            return redirect("medicine-detail", pk=self.object_list.first().pk)

        return response


class MedicineDetailView(UserOnlyMixin, DetailView):
    model = Medicine

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["schedules_active"] = Schedule.objects.active(self.object)
        data["schedules_future"] = Schedule.objects.future(self.object)
        data["schedules_past"] = Schedule.objects.past(self.object)
        return data


class MedicineCreateView(UserOnlyMixin, CreateView):
    model = Medicine
    fields = ["name"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(
            self.request,
            fui_msg_text(
                "Medicine Created",
                "Oh goody. Another medicine! Is that good or bad?",
            ),
        )
        return super().form_valid(form)


class MedicineUpdateView(UserOnlyMixin, UpdateView):
    model = Medicine
    fields = ["name"]

    def get_success_url(self):
        messages.success(
            self.request,
            fui_msg_text(
                "Medicine Updated",
                "That medicine wasn't quite perfect, but your changes should make it all better!",
            ),
        )
        return super().get_success_url()


class MedicineDeleteView(UserOnlyMixin, DeleteView):
    model = Medicine
    success_url = reverse_lazy("medicine-index")

    def get_success_url(self):
        messages.success(
            self.request,
            fui_msg_text(
                "Medicine Deleted",
                "Medicine gone. Poof. Just like that.",
            ),
        )
        return super().get_success_url()


class ConsumptionCreateView(
    WhenFieldMixin,
    ChildUserOnlyMixin,
    MedicineFormMixin,
    MedicineContextMixin,
    MedicineSuccessMixin,
    CreateView,
):
    model = Consumption
    fields = ("when", "quantity")

    def get_initial(self):
        initial = super().get_initial()
        initial["quantity"] = 1
        initial["when"] = localtime()
        return initial

    def get_success_url(self):
        messages.success(
            self.request,
            fui_msg_text(
                "Consumption Created",
                "Nice! Remembering your medication, one day at a time.",
            ),
        )
        return super().get_success_url()


class ConsumptionCreateDefaultView(View):
    def post(self, request, *args, **kwargs):
        medicine = get_object_or_404(
            Medicine, pk=self.kwargs["medicinepk"], user=self.request.user
        )
        Consumption.objects.create(
            medicine=medicine,
            when=localtime(),
            quantity=medicine.default_consumption_quantity,
        )
        messages.success(
            self.request,
            fui_msg_text(
                "Default Consumption Logged",
                "Look at all the time you saved! You should now see your hard work all ready.",
            ),
        )
        return redirect("medicine-detail", pk=medicine.pk)


class ConsumptionUpdateView(
    WhenFieldMixin,
    ChildUserOnlyMixin,
    MedicineContextMixin,
    MedicineSuccessMixin,
    UpdateView,
):
    model = Consumption
    fields = ("when", "quantity")

    def get_success_url(self):
        messages.success(
            self.request,
            fui_msg_text(
                "Consumption Updated",
                "Your consumption change is noted. Thanks!",
            ),
        )
        return super().get_success_url()


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

    def get_success_url(self):
        messages.success(
            self.request,
            fui_msg_text(
                "Schedule Created",
                "Making it happen. Your schedule is now in place.",
            ),
        )
        return super().get_success_url()


class ScheduleUpdateView(
    ChildUserOnlyMixin, MedicineContextMixin, MedicineSuccessMixin, UpdateView
):
    model = Schedule
    form_class = ScheduleForm

    def get_success_url(self):
        messages.success(
            self.request,
            fui_msg_text(
                "Schedule Updated",
                "Those schedule changes have been noted.",
            ),
        )
        return super().get_success_url()


class ScheduleDeleteView(ChildUserOnlyMixin, MedicineSuccessMixin, DeleteView):
    model = Schedule

    def get_success_url(self):
        messages.success(
            self.request,
            fui_msg_text(
                "Schedule Deleted",
                "Well that schedule's gone. Didn't like it, huh?",
            ),
        )
        return super().get_success_url()


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
