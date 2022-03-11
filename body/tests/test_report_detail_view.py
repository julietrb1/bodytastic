from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_body_area, create_entry, create_report
from body.urls.mybody import REPORT_DETAIL_ROUTE
from freezegun import freeze_time


@freeze_time("2022-03-01")
class ReportDetailViewTests(LoginTestCase):
    def test_report_detail_redirects_to_login(self):
        self.client.logout()
        self.verify_redirect(REPORT_DETAIL_ROUTE, {"pk": 1})

    def test_no_other_user_reports_shown(self):
        other_report = create_report(self.other_user)
        response = self.client.get(reverse(REPORT_DETAIL_ROUTE, args=[other_report.pk]))
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_report_404(self):
        response = self.client.get(reverse(REPORT_DETAIL_ROUTE, args=[12345]))
        self.assertEqual(response.status_code, 404)

    def test_report_without_entries(self):
        report = create_report(self.user)
        response = self.client.get(reverse(REPORT_DETAIL_ROUTE, args=[report.pk]))
        self.assertContains(response, "1 Jan 2022")
        self.assertContains(response, "No entries for 1 Jan 2022")

    def test_report_with_entry(self):
        report = create_report(self.user)
        create_entry(report, create_body_area())
        response = self.client.get(reverse(REPORT_DETAIL_ROUTE, args=[report.pk]))
        self.assertContains(response, "Sample Area")
        self.assertContains(response, "20 cm")
