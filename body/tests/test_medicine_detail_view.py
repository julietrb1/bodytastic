from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from django.utils.timezone import make_aware, timedelta, datetime, localtime

from body.tests.model_helpers import (
    create_consumption,
    create_ledger_entry,
    create_medicine,
    create_schedule,
)
from body.urls.medication import MEDICINE_DETAIL_ROUTE
from freezegun import freeze_time


@freeze_time(make_aware(datetime(2022, 3, 1)))
class MedicineDetailViewTests(LoginTestCase):
    def test_with_refills(self):
        """
        Given a medicine with refills,
        those refills should show in a table.
        """
        medicine = create_medicine(self.user, current_balance=1)
        create_ledger_entry(medicine, 5)
        response = self.client.get(reverse(MEDICINE_DETAIL_ROUTE, args=[medicine.pk]))
        self.assertContains(response, "5 (5 left)")

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
            localtime() - timedelta(days=1),
            localtime() + timedelta(days=1),
        )
        response = self.client.get(reverse(MEDICINE_DETAIL_ROUTE, args=[medicine.pk]))
        self.assertContains(response, "Every one day")
        self.assertContains(response, "Next:")
        self.assertContains(response, "2:25 p.m.")

    def test_with_schedule_without_end_date(self):
        medicine = create_medicine(self.user)
        create_schedule(
            medicine,
            localtime() - timedelta(days=1),
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
            localtime() - timedelta(days=2),
            localtime() - timedelta(days=1),
        )
        response = self.client.get(reverse(MEDICINE_DETAIL_ROUTE, args=[medicine.pk]))
        self.assertContains(response, "Finished:")

    def test_with_schedule_without_end_date_in_future(self):
        medicine = create_medicine(self.user)
        create_schedule(
            medicine,
            localtime() + timedelta(days=1),
            localtime() + timedelta(days=2),
        )
        response = self.client.get(reverse(MEDICINE_DETAIL_ROUTE, args=[medicine.pk]))
        self.assertContains(response, "Starts:")
