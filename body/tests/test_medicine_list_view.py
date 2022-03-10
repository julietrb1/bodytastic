from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_medicine, create_schedule


MEDICINE_LIST_ROUTE = "medicine-index"


class MedicineListViewTests(LoginTestCase):
    def test_no_medicines(self):
        """
        If no medicines exist, the empty state is shown.
        """
        response = self.client.get(reverse(MEDICINE_LIST_ROUTE))
        self.assertContains(response, "The Potential for Medicine Is Upon Us.")
        self.assertQuerysetEqual(response.context["object_list"], [])

    def test_one_medicine(self):
        medicine = create_medicine(self.user)
        response = self.client.get(reverse(MEDICINE_LIST_ROUTE))
        self.assertContains(response, medicine.name)
        self.assertContains(response, "0 left")
