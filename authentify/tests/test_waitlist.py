from .test_setup import TestSetUp
from ..models import Waitlist


class TestWaitlist(TestSetUp):

    def test_join_waitlist_adds_new_email(self):
        email = self.user_data['email']
        response = self.client.post(self.waitlist_url, {
            "email": email
        })
        email_test = Waitlist.objects.get(email=email)
        self.assertEqual(response.status_code, 201)
        self.assertEqual((response.json())[
                         'message'], "email successfully submitted")
        self.assertEqual(email_test.email, email)

    def test_join_waitlist_cannot_add_no_data(self):
        response = self.client.post(self.waitlist_url)
        self.assertEqual(response.status_code, 400)

    def test_join_waitlist_cannot_save_duplicates(self):

        response1 = self.client.post(self.waitlist_url, {
            "email": self.user_data['email']
        })
        response2 = self.client.post(self.waitlist_url, {
            "email": self.user_data['email']
        })

        email_test = Waitlist.objects.filter(email=self.user_data['email'])
        self.assertEqual(email_test.count(), 1)
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(
            (response1.json()['message']), "email successfully submitted")
        self.assertEqual(
            (response2.json()['message']), "email already joined waitlist")
