from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_body_area, create_entry, create_report
from django.utils.timezone import localtime, make_aware, datetime

from body.urls.mybody import REPORT_LIST_ROUTE
from freezegun import freeze_time


@freeze_time(make_aware(datetime(2022, 3, 1)))
class ReportListViewTests(LoginTestCase):
    def test_report_list_redirects_to_login(self):
        self.client.logout()
        self.verify_redirect(REPORT_LIST_ROUTE)

    def test_no_reports(self):
        """
        If no reports exist, the empty state is shown.
        """
        response = self.client.get(reverse(REPORT_LIST_ROUTE))
        self.assertContains(response, "No Reports Here, but There Could Be...")
        self.assertQuerysetEqual(response.context["object_list"], [])

    def test_one_report_no_entries(self):
        """
        If a report exists, it should be shown in the list with the no entries message.
        """
        report = create_report(self.user)
        response = self.client.get(reverse(REPORT_LIST_ROUTE))
        self.assertContains(response, "1 Jan 2022")
        self.assertContains(response, "50.5 kg")
        self.assertContains(response, "0 entries")
        self.assertQuerysetEqual(response.context["object_list"], [report])

    def test_one_report_shows_graph(self):
        """
        A recent report should show the summary chart.
        """
        create_report(self.user, localtime())
        response = self.client.get(reverse(REPORT_LIST_ROUTE))
        self.assertIsNotNone(response.context["summary_chart_data"])

    def test_one_report_with_entries_shows_graph(self):
        """
        A recent report with entries should show the summary chart.
        """
        report = create_report(self.user, localtime())
        body_area = create_body_area()
        create_entry(report, body_area)
        response = self.client.get(reverse(REPORT_LIST_ROUTE))
        self.assertIsNotNone(response.context["summary_chart_data"])

    def test_one_report_with_entry(self):
        """
        If a report exists, it should be shown in the list with one entry.
        """
        report = create_report(self.user)
        body_area = create_body_area()
        create_entry(report, body_area)
        response = self.client.get(reverse(REPORT_LIST_ROUTE))
        self.assertContains(response, "1 Jan 2022")
        self.assertContains(response, "50.5 kg")
        self.assertContains(response, "One entry")
        self.assertContains(response, body_area.name)
        self.assertNotContains(response, "WHR:")
        self.assertQuerysetEqual(response.context["object_list"], [report])

    def test_one_report_with_whr_entry(self):
        """
        A report with Hips and Waist entries should show WHR.
        """
        report = create_report(self.user)
        waist_body_area = create_body_area("Waist")
        create_entry(report, waist_body_area, 50)
        hips_body_area = create_body_area("Hips")
        create_entry(report, hips_body_area, 85)
        response = self.client.get(reverse(REPORT_LIST_ROUTE))
        self.assertContains(response, "Two entries")
        self.assertContains(response, "Waist")
        self.assertContains(response, "Hips")
        self.assertContains(response, "WHR: 0.588")
        self.assertQuerysetEqual(response.context["object_list"], [report])

    def test_no_other_user_reports_shown(self):
        report = create_report(self.user)
        create_report(self.other_user)
        response = self.client.get(reverse(REPORT_LIST_ROUTE))
        self.assertQuerysetEqual(response.context["object_list"], [report])
