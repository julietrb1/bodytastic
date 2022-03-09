from django.test import override_settings
from django.contrib.auth.models import User
from django.utils.timezone import datetime, make_aware
from django.test import Client, TestCase
from django.urls import reverse

from mind_and_soul.models import EmotionReport


def create_user(
    username="john", email="lennon@thebeatles.com", password="johnpassword"
):
    return User.objects.create_user(username, email, password)


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
        self.user = create_user()
        self.logged_in = self.client.force_login(self.user)


class UserOnlyMixin:
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ReportListViewTests(LoginTestCase):
    def test_empty_state_shown(self):
        response = self.client.get(reverse("mind_and_soul:report-index"))
        self.assertContains(response, "My Mind &amp; Soul")
        self.assertContains(response, "Mind Over Matter. That's What They Say, Anyway.")

    def test_no_other_user_reports_shown(self):
        report = create_report(self.user)
        create_report(create_user("jane", "jane@example.com", "janepassword"))
        response = self.client.get(reverse("mind_and_soul:report-index"))
        self.assertQuerysetEqual(response.context["object_list"], [report])


class ReportDetailViewTests(LoginTestCase):
    def test_no_other_user_reports_shown(self):
        other_report = create_report(
            create_user("jane", "jane@example.com", "janepassword")
        )
        response = self.client.get(
            reverse("mind_and_soul:report-detail", args=[other_report.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_report_404(self):
        response = self.client.get(reverse("mind_and_soul:report-detail", args=[12345]))
        self.assertEqual(response.status_code, 404)

    def test_report_without_entries(self):
        report = create_report(self.user)
        response = self.client.get(
            reverse("mind_and_soul:report-detail", args=[report.pk])
        )
        self.assertContains(response, "1 Jan 2022")
