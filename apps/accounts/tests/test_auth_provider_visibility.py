from django.test import TestCase, override_settings
from django.urls import reverse


class GoogleAuthProviderVisibilityTests(TestCase):
    @override_settings(GOOGLE_AUTH_CLIENT_ID="", GOOGLE_AUTH_CLIENT_SECRET="")
    def test_login_and_signup_hide_google_when_credentials_are_missing(self):
        for route_name in ("account_login", "account_signup"):
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))

                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, "Continue with Google")
                self.assertNotContains(response, "/accounts/google/login/")

    @override_settings(GOOGLE_AUTH_CLIENT_ID="client-id", GOOGLE_AUTH_CLIENT_SECRET="client-secret")
    def test_login_and_signup_show_google_when_credentials_are_complete(self):
        for route_name in ("account_login", "account_signup"):
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Continue with Google")
                self.assertContains(response, "/accounts/google/login/")
