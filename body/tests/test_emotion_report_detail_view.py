from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_emotion_report
from body.urls.mind_and_soul import EMOTION_REPORT_DETAIL_ROUTE
from freezegun import freeze_time


@freeze_time("2022-03-01")
class EmotionReportDetailViewTests(LoginTestCase):
    def test_no_other_user_reports_shown(self):
        other_report = create_emotion_report(self.other_user)
        response = self.client.get(
            reverse(EMOTION_REPORT_DETAIL_ROUTE, args=[other_report.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_report_404(self):
        response = self.client.get(reverse(EMOTION_REPORT_DETAIL_ROUTE, args=[12345]))
        self.assertEqual(response.status_code, 404)

    def test_report_without_entries(self):
        report = create_emotion_report(self.user)
        response = self.client.get(
            reverse(EMOTION_REPORT_DETAIL_ROUTE, args=[report.pk])
        )
        self.assertContains(response, "1 Jan 2022")
