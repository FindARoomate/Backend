from django.urls import reverse

from rest_framework.test import APITestCase

from authentify.models import Waitlist
from authentify.serializers import WaitlistSerializer


class TestViews(APITestCase):
    """
    The class to test my JoinWaitlist API endpoint
    """

    def setUp(self):
        self.waitlist_url = reverse('authentify:join_waitlist')
        self.email = "testuser@gmail.com"

    def test_join_waitlist_adds_new_email(self):

        response = self.client.post(self.waitlist_url, {
            "email": self.email
        })

        email_test = Waitlist.objects.get(email=self.email)
        self.assertEqual(response.status_code, 201)
        self.assertEqual((response.json())[
                         "message"], WaitlistSerializer.message)
        self.assertEqual(email_test.email, self.email)

    def test_join_waitlist_cannot_add_no_data(self):
        response = self.client.post(self.waitlist_url)
        self.assertEqual(response.status_code, 400)

    def test_join_waitlist_cannot_save_duplicates(self):

        response1 = self.client.post(self.waitlist_url, {
            "email": self.email
        })
        response2 = self.client.post(self.waitlist_url, {
            "email": self.email
        })

        email_test = Waitlist.objects.filter(email=self.email)
        self.assertEqual(email_test.count(), 1)
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 201)