from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class HomeViewTests(TestCase):
    def test_about_page_view(self):
        url = reverse("about")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/about.html")
        self.assertContains(response, "ABOUT PAGE")
