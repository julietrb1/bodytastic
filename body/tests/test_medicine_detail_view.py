from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from django.utils.timezone import datetime, make_aware, timedelta

from body.tests.model_helpers import (
    create_consumption,
    create_medicine,
    create_schedule,
)
from body.urls.medication import MEDICINE_DETAIL_ROUTE
from freezegun import freeze_time


@freeze_time("2022-03-01")
class MedicineDetailViewTests(LoginTestCase):
    def test_with_consumptions(self):
        """
        Given that a consumption exists for a medicine, it should be shown in the view.
        """
        medicine = create_medicine(self.user, current_balance=1)
        create_consumption(medicine)
        response = self.client.get(reverse(MEDICINE_DETAIL_ROUTE, args=[medicine.pk]))
        self.assertContains(response, "1 Jan 2022")
        self.assertContains(response, "2:25 p.m.")

    def test_with_schedule(self):
        medicine = create_medicine(self.user)
        create_schedule(
            medicine,
            make_aware(datetime.now() - timedelta(days=1)),
            make_aware(datetime.now() + timedelta(days=1)),
        )
        response = self.client.get(reverse(MEDICINE_DETAIL_ROUTE, args=[medicine.pk]))
        self.assertContains(response, "Every one day")
        self.assertContains(response, "Next:")
        self.assertContains(response, "2:25 p.m.")

    def test_with_schedule_without_end_date(self):
        medicine = create_medicine(self.user)
        create_schedule(
            medicine,
            make_aware(datetime.now() - timedelta(days=1)),
            None,
        )
        response = self.client.get(reverse(MEDICINE_DETAIL_ROUTE, args=[medicine.pk]))
        self.assertContains(response, "Every one day")
        self.assertContains(response, "Next:")
        self.assertContains(response, "2:25 p.m.")

    def test_with_schedule_without_end_date_in_past(self):
        medicine = create_medicine(self.user)
        create_schedule(
            medicine,
            make_aware(datetime.now() - timedelta(days=2)),
            make_aware(datetime.now() - timedelta(days=1)),
        )
        response = self.client.get(reverse(MEDICINE_DETAIL_ROUTE, args=[medicine.pk]))
        self.assertContains(response, "Finished:")

    def test_with_schedule_without_end_date_in_future(self):
        medicine = create_medicine(self.user)
        create_schedule(
            medicine,
            make_aware(datetime.now() + timedelta(days=1)),
            make_aware(datetime.now() + timedelta(days=2)),
        )
        response = self.client.get(reverse(MEDICINE_DETAIL_ROUTE, args=[medicine.pk]))
        self.assertContains(response, "Starts:")
