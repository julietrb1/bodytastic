from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils.timezone import datetime
from body.forms import ReportForm

from body.models import BodyArea, Report, Entry


class UserOnlyMixin:
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class EntryUserOnlyMixin:
    def get_queryset(self):
        return self.model.objects.filter(report__user=self.request.user)


class BodyAreaMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["body_areas"] = BodyArea.objects.all()
        return context


class TodayMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = datetime.today().date()
        return context


class EntrySuccessMixin:
    def get_success_url(self) -> str:
        return reverse_lazy("body:report-detail", kwargs={"pk": self.object.report.pk})


class ReportListView(UserOnlyMixin, BodyAreaMixin, TodayMixin, ListView):
    model = Report


class ReportDetailView(UserOnlyMixin, BodyAreaMixin, DetailView):
    model = Report


class ReportCreateView(UserOnlyMixin, CreateView):
    model = Report
    form_class = ReportForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReportUpdateView(UserOnlyMixin, UpdateView):
    model = Report
    fields = ["weight_in_kg"]


class ReportDeleteView(UserOnlyMixin, DeleteView):
    model = Report

    def get_success_url(self) -> str:
        return reverse_lazy("body:report-index")


class EntryReportMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = Report.objects.get(pk=self.kwargs["reportpk"])
        context["report"] = report
        return context


class EntryCreateView(
    EntryUserOnlyMixin, EntrySuccessMixin, EntryReportMixin, CreateView
):
    model = Entry
    fields = ["body_area", "measurement", "sensations", "notes"]

    def form_valid(self, form):
        report = Report.objects.get(pk=self.kwargs["reportpk"])
        form.instance.report = report
        return super().form_valid(form)


class EntryUpdateView(
    EntryUserOnlyMixin, EntrySuccessMixin, EntryReportMixin, UpdateView
):
    model = Entry
    fields = ["measurement", "sensations", "notes"]


class EntryDeleteView(EntryUserOnlyMixin, EntrySuccessMixin, DeleteView):
    model = Entry
