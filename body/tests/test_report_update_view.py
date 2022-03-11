from decimal import Decimal
from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_report
from body.models import Report
from body.urls.mybody import REPORT_UPDATE_ROUTE


class ReportUpdateViewTests(LoginTestCase):
    def test_no_other_user_reports_shown(self):
        other_report = create_report(self.other_user)
        response = self.client.get(reverse(REPORT_UPDATE_ROUTE, args=[other_report.pk]))
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_report_404(self):
        response = self.client.get(reverse(REPORT_UPDATE_ROUTE, args=[12345]))
        self.assertEqual(response.status_code, 404)

    def test_valid_report_loads_form(self):
        report = create_report(self.user)
        response = self.client.get(reverse(REPORT_UPDATE_ROUTE, args=[report.pk]))
        self.assertContains(response, "Edit")
        self.assertEqual(
            response.context["form"].initial["weight_in_kg"], Decimal(50.5)
        )

    def test_updating_report_saves(self):
        report = create_report(self.user)
        new_weight = 90
        response = self.client.post(
            reverse(REPORT_UPDATE_ROUTE, args=[report.pk]),
            {
                "pk": report.pk,
                "weight_in_kg": new_weight,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        new_report = Report.objects.get(pk=report.pk)
        self.assertEqual(new_report.weight_in_kg, new_weight)

    def test_updating_report_shows_message(self):
        report = create_report(self.user)
        new_weight = 90
        response = self.client.post(
            reverse(REPORT_UPDATE_ROUTE, args=[report.pk]),
            {
                "pk": report.pk,
                "weight_in_kg": new_weight,
            },
            follow=True,
        )
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "A little tuning here and there never hurt anyone. Report changes saved.",
        )
