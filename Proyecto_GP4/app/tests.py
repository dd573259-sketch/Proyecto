from django.test import TestCase
from django.urls import reverse

class BasicTestCase(TestCase):
    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 302])  # 302 si redirige a login

