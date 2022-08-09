"""Imports"""
from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):
    """Test index view"""
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')

    def test_index_GET(self):
        """test index"""
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
