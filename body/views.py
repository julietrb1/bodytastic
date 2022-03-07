from graphlib import CycleError
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils.timezone import datetime
from body.forms import ReportForm
from django.utils.timezone import datetime, timedelta
from django.contrib.humanize.templatetags.humanize import naturalday

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


def report_stats_over_time(last_x_days=14):

    current_date = datetime.now().date()
    last_x_reports = Report.objects.order_by("when").filter(
        when__gt=current_date - timedelta(days=last_x_days)
    )
    if not last_x_days or last_x_days < 0 or not last_x_reports:
        return None

    earliest_date = last_x_reports[0].when
    earliest_days_ago = (current_date - earliest_date).days
    latest_date = last_x_reports[len(last_x_reports) - 1].when
    latest_days_ago = (current_date - latest_date).days
    all_dates = [
        current_date - timedelta(days=subtract_days)
        for subtract_days in list(
            reversed(range(latest_days_ago, earliest_days_ago - 1))
        )
    ]
    all_datasets = [
        {
            "label": "Weight (kg)",
            "borderColor": "#FC814A",
            "backgroundColor": "#FEC8AF",
            "data": [None] * len(all_dates),
            "tension": 0.1,
            "fill": True,
            "spanGaps": True,
        }
    ]
    for report in last_x_reports:
        try:
            idx = all_dates.index(report.when)
            all_datasets[0]["data"][idx] = (
                float(report.weight_in_kg) if report.weight_in_kg else None
            )
        except ValueError:
            pass

    return {
        "labels": [naturalday(d) for d in all_dates],
        "datasets": all_datasets,
    }


class ReportListView(UserOnlyMixin, BodyAreaMixin, TodayMixin, ListView):
    model = Report

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["summary_chart_data"] = report_stats_over_time()
        return context


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
