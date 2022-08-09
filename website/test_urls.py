"""Imports"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from website.views import index


# Create your tests here
class TestUrls(SimpleTestCase):
    """Test urls"""
    def test_index_url_is_resolved(self):
        """Test index"""
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)
