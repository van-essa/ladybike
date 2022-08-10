"""Imports"""
from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):
    """test articles"""

    def setUp(self):
        """test setup"""
        self.client = Client()
        self.articles_url = reverse('articles')
        self.article_detail_url = reverse('article_detail', args=['project1'])

    def test_article_list_GET(self):
        """test list"""
        response = self.client.get(self.articles_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles.html')

    def test_article_detail_GET(self):
        """test detail"""
        response = self.client.get(self.article_detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles.html')
