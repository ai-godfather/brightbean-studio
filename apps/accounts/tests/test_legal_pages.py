from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User


class LegalPagesTests(TestCase):
    pages = (
        ("privacy_policy", "Privacy Policy"),
        ("terms_of_service", "Terms of Service"),
        ("data_deletion", "Data Deletion Instructions"),
    )

    def test_legal_pages_are_public(self):
        for route_name, expected_heading in self.pages:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, expected_heading)
                self.assertContains(response, "admin@shopauth.cloud")

    def test_legal_pages_bypass_tos_acceptance_redirect(self):
        user = User.objects.create_user(email="legal@example.com", password="test-password")
        self.client.force_login(user)

        for route_name, _expected_heading in self.pages:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)
                self.assertNotEqual(response.url if response.status_code == 302 else "", "/accounts/accept-terms/")

    def test_signup_links_to_local_legal_pages(self):
        response = self.client.get(reverse("account_signup"))

        self.assertContains(response, reverse("terms_of_service"))
        self.assertContains(response, reverse("privacy_policy"))
