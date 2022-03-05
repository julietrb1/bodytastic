from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import datetime
from django.test import override_settings
from body.models import BodyArea, Entry, Report


def create_report(user, when=datetime(2022, 1, 1), weight_in_kg=50.5):
    return Report.objects.create(user=user, when=when, weight_in_kg=weight_in_kg)


def create_entry(report, body_area, measurement=20):
    return Entry.objects.create(
        report=report, body_area=body_area, measurement=measurement
    )


def create_body_area(name="Sample Area", measurement_unit="cm"):
    return BodyArea.objects.create(name=name, measurement_unit=measurement_unit)


@override_settings(AXES_HANDLER="axes.handlers.dummy.AxesDummyHandler")
class ReportListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            "john", "lennon@thebeatles.com", "johnpassword"
        )
        self.logged_in = self.client.force_login(self.user)

    def test_no_reports(self):
        """
        If no reports exist, the empty state is shown.
        """
        response = self.client.get(reverse("body:report-index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Reports Here, but There Could Be...")
        self.assertQuerysetEqual(response.context["object_list"], [])

    def test_one_report_no_entries(self):
        """
        If a report exists, it should be shown in the list with the no entries message.
        """
        report = create_report(self.user)
        response = self.client.get(reverse("body:report-index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1 Jan 2022")
        self.assertContains(response, "50.5 kg")
        self.assertContains(response, "0 entries")
        self.assertQuerysetEqual(response.context["object_list"], [report])

    def test_one_report_with_entry(self):
        """
        If a report exists, it should be shown in the list with one entry.
        """
        report = create_report(self.user)
        body_area = create_body_area()
        create_entry(report, body_area)
        response = self.client.get(reverse("body:report-index"))
        self.assertEqual(response.status_code, 200)
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
        response = self.client.get(reverse("body:report-index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1 Jan 2022")
        self.assertContains(response, "50.5 kg")
        self.assertContains(response, "Two entries")
        self.assertContains(response, "Waist")
        self.assertContains(response, "Hips")
        self.assertContains(response, "WHR: 0.588")
        self.assertQuerysetEqual(response.context["object_list"], [report])
