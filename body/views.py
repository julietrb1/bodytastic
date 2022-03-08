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
import random


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


def generate_data(label, colour_pair_idx, data_length):
    return {
        "backgroundColor": f"rgba({COLOUR_PAIRS[colour_pair_idx]}, 0.24)",
        "borderColor": f"rgb({COLOUR_PAIRS[colour_pair_idx]})",
        "data": [None] * data_length,
        "elements": {
            "point": {"pointStyle": "crossRot", "radius": 6, "borderWidth": 2}
        },
        "fill": False,
        "label": label,
        "spanGaps": True,
        "tension": 0.1,
    }


def add_entries(date_idx, entries, all_datasets, data_length):
    for entry in entries:
        label_name = f"{entry.body_area.name} ({entry.body_area.measurement_unit})"
        dataset_idx = -1
        try:
            dataset_idx = list(map(lambda x: x["label"], all_datasets)).index(
                label_name
            )
        except ValueError:
            pass

        if dataset_idx == -1:
            all_datasets.append(
                generate_data(
                    label_name,
                    len(all_datasets) % len(COLOUR_PAIRS),
                    data_length,
                )
            )

        all_datasets[dataset_idx]["data"][date_idx] = (
            float(entry.measurement) if entry.measurement else None
        )


COLOUR_PAIRS = [
    "249, 65, 68",
    "243, 114, 44",
    "248, 150, 30",
    "249, 132, 74",
    "249, 199, 79",
    "144, 190, 109",
    "67, 170, 139",
    "77, 144, 142",
    "87, 117, 144",
    "39, 125, 161",
]
random.shuffle(COLOUR_PAIRS)


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
            reversed(range(latest_days_ago, earliest_days_ago + 1))
        )
    ]
    all_datasets = [
        generate_data(label, idx, len(all_dates))
        for idx, label in enumerate(["Weight (kg)", "WHR x100"])
    ]
    for report in last_x_reports:
        try:
            date_idx = all_dates.index(report.when)
            all_datasets[0]["data"][date_idx] = (
                float(report.weight_in_kg) if report.weight_in_kg else None
            )
            all_datasets[1]["data"][date_idx] = (
                float(report.waist_hip_ratio * 100) if report.waist_hip_ratio else None
            )
            add_entries(date_idx, report.entry_set.all(), all_datasets, len(all_dates))
        except ValueError:
            pass

    filtered_datasets = list(
        filter(lambda x: any(d is not None for d in x["data"]), all_datasets)
    )

    return {
        "labels": [naturalday(d) for d in all_dates],
        "datasets": filtered_datasets,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["disabled_dates"] = Report.objects.filter(
            user=self.request.user
        ).values_list("when", flat=True)
        return context

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
