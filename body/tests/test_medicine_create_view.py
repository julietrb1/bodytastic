from django.urls import reverse
from body.tests.login_test_case import LoginTestCase


MEDICINE_CREATE_ROUTE = "medicine-create"


class MedicineCreateViewTests(LoginTestCase):
    def test_create_form_shows_name_field(self):
        response = self.client.get(reverse(MEDICINE_CREATE_ROUTE))
        self.assertContains(response, "Name:")
