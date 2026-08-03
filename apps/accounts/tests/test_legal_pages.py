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

    def test_google_and_youtube_disclosures_are_public(self):
        privacy = self.client.get(reverse("privacy_policy"))
        self.assertContains(privacy, "Google API Services User Data Policy")
        self.assertContains(privacy, "including the Limited Use requirements")
        self.assertContains(privacy, "Google Privacy Policy")
        self.assertContains(privacy, "security.google.com/settings/security/permissions")
        self.assertContains(privacy, "delete the associated YouTube API data no later than 30 days")

        terms = self.client.get(reverse("terms_of_service"))
        self.assertContains(terms, "YouTube Terms of Service")
        self.assertContains(terms, "YouTube API Services Developer Policies")

        deletion = self.client.get(reverse("data_deletion"))
        self.assertContains(deletion, "Google's third-party connections settings")
        self.assertContains(deletion, "associated YouTube API data is deleted within 30 days")

        product_page = self.client.get(reverse("youtube_integration"))
        self.assertEqual(product_page.status_code, 200)
        self.assertContains(
            product_page,
            "<title>BrightBean Social Studio — YouTube Publishing and Analytics · BrightBean Social Studio</title>",
            html=True,
        )
        self.assertContains(product_page, "<h1>BrightBean Social Studio</h1>", html=True)
        self.assertContains(product_page, 'alt="BrightBean Social Studio"')
        self.assertContains(product_page, "BrightBean Social Studio helps individual creators")
        self.assertContains(product_page, "accesses the selected channel identity")
        self.assertContains(product_page, "never publishes")
        self.assertContains(product_page, "content or changes visibility without an explicit user action")
        self.assertContains(product_page, reverse("privacy_policy"))
        self.assertContains(product_page, reverse("terms_of_service"))
        self.assertContains(product_page, reverse("data_deletion"))

    def test_individual_operator_and_subscription_disclosures_are_public(self):
        for route_name in ("privacy_policy", "terms_of_service", "data_deletion"):
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertContains(response, "Piotr Kwiatkowski")
                self.assertContains(response, "ul. Ludowa 9A")
                self.assertContains(response, "August 3, 2026")

        privacy = self.client.get(reverse("privacy_policy"))
        self.assertContains(privacy, "payment-processor customer or checkout identifiers")
        self.assertContains(privacy, "Stripe processes checkout and subscription payments")

        terms = self.client.get(reverse("terms_of_service"))
        self.assertContains(terms, "BrightBean Studio uses a freemium model")
        self.assertContains(terms, "successive monthly billing periods")
