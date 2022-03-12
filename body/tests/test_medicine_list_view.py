from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_medicine
from body.urls.medication import MEDICINE_DETAIL_ROUTE, MEDICINE_LIST_ROUTE
from freezegun import freeze_time


@freeze_time("2022-03-01")
class MedicineListViewTests(LoginTestCase):
    def test_no_medicines(self):
        response = self.client.get(reverse(MEDICINE_LIST_ROUTE))
        self.assertContains(response, "The Potential for Medicine Is Upon Us.")
        self.assertQuerysetEqual(response.context["object_list"], [])

    def test_one_medicine_redirects_to_detail(self):
        medicine = create_medicine(self.user)
        response = self.client.get(reverse(MEDICINE_LIST_ROUTE), follow=True)
        self.assertRedirects(
            response, reverse(MEDICINE_DETAIL_ROUTE, args=[medicine.pk])
        )
        self.assert_message(response, "Took a shortcut to the only medicine you have.")

    def test_two_medicines_stays_on_page(self):
        medicine_one = create_medicine(self.user, "Med1")
        medicine_two = create_medicine(self.user, "Med2")
        response = self.client.get(reverse(MEDICINE_LIST_ROUTE))
        self.assertContains(response, medicine_one.name)
        self.assertContains(response, medicine_two.name)
