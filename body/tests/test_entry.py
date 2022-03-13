from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import (
    create_body_area,
    create_entry,
    create_ledger_entry,
    create_report,
)
from freezegun import freeze_time
from django.utils.timezone import make_aware, datetime, localdate, timedelta


@freeze_time(make_aware(datetime(2022, 3, 1)))
class EntryTests(LoginTestCase):
    def test_diff_from_last_with_none(self):
        report = create_report(
            self.user,
        )
        body_area = create_body_area()
        entry = create_entry(report, body_area)
        self.assertIsNone(entry.diff_from_last)

    def test_diff_from_last_with_one(self):
        report_one = create_report(self.user, localdate() - timedelta(days=14))
        report_two = create_report(self.user, localdate())
        body_area = create_body_area()
        entry_one = create_entry(report_one, body_area, 20)
        entry_two = create_entry(report_two, body_area, 22)
        self.assertIsNone(entry_one.diff_from_last)
        self.assertEqual(entry_two.diff_from_last, 2)

    def test_diff_from_last_with_two(self):
        report_one = create_report(self.user, localdate() - timedelta(days=2))
        report_two = create_report(self.user, localdate() - timedelta(days=1))
        report_three = create_report(self.user, localdate())
        body_area = create_body_area()
        entry_one = create_entry(report_one, body_area, 20)
        entry_two = create_entry(report_two, body_area, 22)
        entry_three = create_entry(report_three, body_area, 25)
        self.assertIsNone(entry_one.diff_from_last)
        self.assertEqual(entry_two.diff_from_last, 2)
        self.assertEqual(entry_three.diff_from_last, 3)

    def test_diff_from_last_too_long_ago(self):
        report_one = create_report(self.user, localdate() - timedelta(days=15))
        report_two = create_report(self.user, localdate())
        body_area = create_body_area()
        entry_one = create_entry(report_one, body_area, 20)
        entry_two = create_entry(report_two, body_area, 22)
        self.assertIsNone(entry_one.diff_from_last)
        self.assertIsNone(entry_two.diff_from_last)

    def test_diff_from_last_with_different_body_part(self):
        report_one = create_report(self.user, localdate() - timedelta(days=1))
        report_two = create_report(self.user, localdate())
        body_area_one = create_body_area("B1")
        body_area_two = create_body_area("B2")
        entry_one = create_entry(report_one, body_area_one, 20)
        entry_two = create_entry(report_two, body_area_two, 22)
        self.assertIsNone(entry_one.diff_from_last)
        self.assertIsNone(entry_two.diff_from_last)
