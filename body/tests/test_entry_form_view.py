from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_body_area, create_entry, create_report
from body.urls.mybody import ENTRY_MASS_UPDATE_ROUTE


class EntryFormViewTests(LoginTestCase):
    def test_entry_form_non_existent_report(self):
        response = self.client.get(reverse(ENTRY_MASS_UPDATE_ROUTE, args=[12345]))
        self.assertEqual(response.status_code, 404)

    def test_entry_form_post_non_existent_report(self):
        response = self.client.post(reverse(ENTRY_MASS_UPDATE_ROUTE, args=[12345]))
        self.assertEqual(response.status_code, 404)

    def test_entry_form_shows_empty(self):
        create_body_area()
        report = create_report(self.user)
        response = self.client.get(reverse(ENTRY_MASS_UPDATE_ROUTE, args=[report.pk]))
        self.assertEqual(response.context["form"]["Sample Area"].initial, None)

    def test_entry_form_shows_initial(self):
        report = create_report(self.user)
        create_entry(report, create_body_area())
        response = self.client.get(reverse(ENTRY_MASS_UPDATE_ROUTE, args=[report.pk]))
        self.assertEqual(response.context["form"]["Sample Area"].initial, 20)

    def test_entry_form_creates_entry(self):
        body_area = create_body_area()
        report = create_report(self.user)
        self.assertEqual(report.entry_set.count(), 0)
        response = self.client.post(
            reverse(ENTRY_MASS_UPDATE_ROUTE, args=[report.pk]),
            {body_area.name: 50},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(report.entry_set.count(), 1)
        created_entry = report.entry_set.first()
        self.assertEqual(created_entry.measurement, 50)

    def test_entry_form_modifies_entry(self):
        report = create_report(self.user)
        body_area = create_body_area()
        create_entry(report, body_area)
        self.assertEqual(report.entry_set.count(), 1)
        response = self.client.post(
            reverse(ENTRY_MASS_UPDATE_ROUTE, args=[report.pk]),
            {body_area.name: 50},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(report.entry_set.count(), 1)
        modified_entry = report.entry_set.first()
        self.assertEqual(modified_entry.measurement, 50)

    def test_entry_form_deletes_entry(self):
        report = create_report(self.user)
        body_area = create_body_area()
        create_entry(report, body_area)
        self.assertEqual(report.entry_set.count(), 1)
        response = self.client.post(
            reverse(ENTRY_MASS_UPDATE_ROUTE, args=[report.pk]),
            {body_area.name: ""},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(report.entry_set.count(), 0)
