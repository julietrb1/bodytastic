from body.models import BodyArea
from body.models.entry import Entry
from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_report
from freezegun import freeze_time
from django.utils.timezone import make_aware, datetime

BRA_SIZE_TEST_COMBOS = (
    (64, 76, None),
    (65, 93, None),
    (65, 76, "8AA"),
    (65, 77, "8A"),
    (70, 78, "8A"),
    (65, 79, "8B"),
    (70, 80, "8B"),
    (65, 81, "8C"),
    (70, 82, "8C"),
    (65, 83, "8D"),
    (70, 84, "8D"),
    (65, 85, "8E"),
    (70, 86, "8E"),
    (65, 87, "8F"),
    (70, 88, "8F"),
    (65, 89, "8G"),
    (70, 90, "8G"),
    (71, 81, "10AA"),
    (71, 82, "10A"),
    (76, 83, "10A"),
    (71, 84, "10B"),
    (72, 85, "10B"),
)


@freeze_time(make_aware(datetime(2022, 3, 1)))
class ReportTests(LoginTestCase):
    def test_bra_sizes(self):
        """
        Given bust and under bust measurements,
        when calling the bra_size property on a Report,
        then the correct size should be reported on size boundaries.
        """
        report = create_report(self.user)
        bust_body_area = BodyArea.objects.get(name="Bust")
        under_bust_body_area = BodyArea.objects.get(name="Under bust")
        for (
            under_bust_measurement,
            bust_measurement,
            expected_bra_size,
        ) in BRA_SIZE_TEST_COMBOS:
            Entry.objects.update_or_create(
                report=report,
                body_area=under_bust_body_area,
                defaults={"measurement": under_bust_measurement},
            )
            Entry.objects.update_or_create(
                report=report,
                body_area=bust_body_area,
                defaults={"measurement": bust_measurement},
            )
            self.assertEqual(report.bra_size, expected_bra_size)
