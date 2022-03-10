from django.test import override_settings
from django.contrib.auth.models import User
from django.utils.timezone import datetime, make_aware
from django.test import Client, TestCase
from django.urls import reverse

from mind_and_soul.models import EmotionReport

EMOTION_REPORT_LIST_ROUTE = "mind_and_soul:report-index"
EMOTION_REPORT_DETAIL_ROUTE = "mind_and_soul:report-detail"


def create_report(
    user, when=make_aware(datetime(2022, 1, 1)), energy_level=5, notes=""
):
    return EmotionReport.objects.create(
        user=user, when=when, energy_level=energy_level, notes=notes
    )


@override_settings(AXES_HANDLER="axes.handlers.dummy.AxesDummyHandler")
class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            "john", "lennon@thebeatles.com", "johnpassword"
        )
        self.other_user = User.objects.create_user(
            "jane", "jane@example.com", "janepassword"
        )
        self.logged_in = self.client.force_login(self.user)


class UserOnlyMixin:
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class EmotionReportListViewTests(LoginTestCase):
    def test_empty_state_shown(self):
        response = self.client.get(reverse(EMOTION_REPORT_LIST_ROUTE))
        self.assertContains(response, "My Mind &amp; Soul")
        self.assertContains(response, "Mind Over Matter. That's What They Say, Anyway.")

    def test_no_other_user_reports_shown(self):
        report = create_report(self.user)
        create_report(self.other_user)
        response = self.client.get(reverse(EMOTION_REPORT_LIST_ROUTE))
        self.assertQuerysetEqual(response.context["object_list"], [report])


class EmotionReportDetailViewTests(LoginTestCase):
    def test_no_other_user_reports_shown(self):
        other_report = create_report(self.other_user)
        response = self.client.get(
            reverse(EMOTION_REPORT_DETAIL_ROUTE, args=[other_report.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_report_404(self):
        response = self.client.get(reverse(EMOTION_REPORT_DETAIL_ROUTE, args=[12345]))
        self.assertEqual(response.status_code, 404)

    def test_report_without_entries(self):
        report = create_report(self.user)
        response = self.client.get(
            reverse(EMOTION_REPORT_DETAIL_ROUTE, args=[report.pk])
        )
        self.assertContains(response, "1 Jan 2022")
