from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_emotion_report
from body.urls.mind_and_soul import EMOTION_REPORT_LIST_ROUTE
from freezegun import freeze_time


@freeze_time("2022-03-01")
class EmotionReportListViewTests(LoginTestCase):
    def test_empty_state_shown(self):
        response = self.client.get(reverse(EMOTION_REPORT_LIST_ROUTE))
        self.assertContains(response, "My Mind &amp; Soul")
        self.assertContains(response, "Mind Over Matter. That's What They Say, Anyway.")

    def test_no_other_user_reports_shown(self):
        report = create_emotion_report(self.user)
        create_emotion_report(self.other_user)
        response = self.client.get(reverse(EMOTION_REPORT_LIST_ROUTE))
        self.assertQuerysetEqual(response.context["object_list"], [report])
