from .test_setup import TestSetUp
from ..models import CustomUser


class TestAuthentication(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        response = self.client.post(self.register_url)

        self.assertEqual(response.status_code, 400)

    def test_user_can_register(self):
        response = self.client.post(
            self.register_url, self.user_data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_user_can_login_after_activation(self):
        response = self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=response.data['email'])
        user.is_active = True
        user.save()

        response2 = self.client.post(self.login_url, {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        }, format="json")

        self.assertEqual(response2.status_code, 200)

    def test_user_cannot_login_after_activation(self):
        self.client.post(self.register_url, self.user_data, format="json")

        response = self.client.post(self.login_url, {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        }, format="json")

        self.assertEqual(response.status_code, 401)