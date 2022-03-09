from decimal import Decimal
from django.test import Client, TestCase, SimpleTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import datetime, make_aware
from django.test import override_settings
from body.models import BodyArea, Entry, Report

LIST_ROUTE_NAME = "body:report-index"
UPDATE_ROUTE_NAME = "body:report-update"
DETAIL_ROUTE_NAME = "body:report-detail"


def create_report(user, when=make_aware(datetime(2022, 1, 1)), weight_in_kg=50.5):
    return Report.objects.create(user=user, when=when, weight_in_kg=weight_in_kg)


def create_entry(report, body_area, measurement=20):
    return Entry.objects.create(
        report=report, body_area=body_area, measurement=measurement
    )


def create_body_area(name="Sample Area", measurement_unit="cm"):
    return BodyArea.objects.create(name=name, measurement_unit=measurement_unit)


def create_user(
    username="john", email="lennon@thebeatles.com", password="johnpassword"
):
    return User.objects.create_user(username, email, password)


@override_settings(AXES_HANDLER="axes.handlers.dummy.AxesDummyHandler")
class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_user()
        self.logged_in = self.client.force_login(self.user)


class ViewsWithoutLoginTests(SimpleTestCase):
    def verify_redirect(self, route_path, kwargs=None):
        route_path = reverse(route_path, kwargs=kwargs)
        response = self.client.get(route_path)
        self.assertRedirects(
            response,
            f"/accounts/login/?next={route_path}",
            fetch_redirect_response=False,
        )

    def test_report_list_redirects_to_login(self):
        self.verify_redirect(LIST_ROUTE_NAME)

    def test_report_detail_redirects_to_login(self):
        self.verify_redirect(DETAIL_ROUTE_NAME, {"pk": 1})


class ReportListViewTests(LoginTestCase):
    def test_no_reports(self):
        """
        If no reports exist, the empty state is shown.
        """
        response = self.client.get(reverse(LIST_ROUTE_NAME))
        self.assertContains(response, "No Reports Here, but There Could Be...")
        self.assertQuerysetEqual(response.context["object_list"], [])

    def test_one_report_no_entries(self):
        """
        If a report exists, it should be shown in the list with the no entries message.
        """
        report = create_report(self.user)
        response = self.client.get(reverse(LIST_ROUTE_NAME))
        self.assertContains(response, "1 Jan 2022")
        self.assertContains(response, "50.5 kg")
        self.assertContains(response, "0 entries")
        self.assertQuerysetEqual(response.context["object_list"], [report])

    def test_one_report_shows_graph(self):
        """
        A recent report should show the summary chart.
        """
        create_report(self.user, datetime.now())
        response = self.client.get(reverse(LIST_ROUTE_NAME))
        self.assertIsNotNone(response.context["summary_chart_data"])

    def test_one_report_with_entries_shows_graph(self):
        """
        A recent report with entries should show the summary chart.
        """
        report = create_report(self.user, datetime.now())
        body_area = create_body_area()
        create_entry(report, body_area)
        response = self.client.get(reverse(LIST_ROUTE_NAME))
        self.assertIsNotNone(response.context["summary_chart_data"])

    def test_one_report_with_entry(self):
        """
        If a report exists, it should be shown in the list with one entry.
        """
        report = create_report(self.user)
        body_area = create_body_area()
        create_entry(report, body_area)
        response = self.client.get(reverse(LIST_ROUTE_NAME))
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
        response = self.client.get(reverse(LIST_ROUTE_NAME))
        self.assertContains(response, "1 Jan 2022")
        self.assertContains(response, "50.5 kg")
        self.assertContains(response, "Two entries")
        self.assertContains(response, "Waist")
        self.assertContains(response, "Hips")
        self.assertContains(response, "WHR: 0.588")
        self.assertQuerysetEqual(response.context["object_list"], [report])

    def test_no_other_user_reports_shown(self):
        report = create_report(self.user)
        create_report(create_user("jane", "jane@example.com", "janepassword"))
        response = self.client.get(reverse(LIST_ROUTE_NAME))
        self.assertQuerysetEqual(response.context["object_list"], [report])


class ReportDetailViewTests(LoginTestCase):
    def test_no_other_user_reports_shown(self):
        other_report = create_report(
            create_user("jane", "jane@example.com", "janepassword")
        )
        response = self.client.get(reverse(DETAIL_ROUTE_NAME, args=[other_report.pk]))
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_report_404(self):
        response = self.client.get(reverse(DETAIL_ROUTE_NAME, args=[12345]))
        self.assertEqual(response.status_code, 404)

    def test_report_without_entries(self):
        report = create_report(self.user)
        response = self.client.get(reverse(DETAIL_ROUTE_NAME, args=[report.pk]))
        self.assertContains(response, "1 Jan 2022")
        self.assertContains(response, "No entries for 1 Jan 2022")

    def test_report_with_entry(self):
        report = create_report(self.user)
        create_entry(report, create_body_area())
        response = self.client.get(reverse(DETAIL_ROUTE_NAME, args=[report.pk]))
        self.assertContains(response, "Sample Area")
        self.assertContains(response, "20 cm")


class ReportUpdateViewTests(LoginTestCase):
    def test_no_other_user_reports_shown(self):
        other_report = create_report(
            create_user("jane", "jane@example.com", "janepassword")
        )
        response = self.client.get(reverse(UPDATE_ROUTE_NAME, args=[other_report.pk]))
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_report_404(self):
        response = self.client.get(reverse(UPDATE_ROUTE_NAME, args=[12345]))
        self.assertEqual(response.status_code, 404)

    def test_valid_report_loads_form(self):
        report = create_report(self.user)
        response = self.client.get(reverse(UPDATE_ROUTE_NAME, args=[report.pk]))
        self.assertContains(response, "Edit")
        self.assertEqual(
            response.context["form"].initial["weight_in_kg"], Decimal(50.5)
        )
