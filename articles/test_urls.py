"""Imports"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from articles.views import PostList, PostDetail, PostLike


# Create your tests here
class TestUrls(SimpleTestCase):
    """Test urls"""
    def test_post_list_url_is_resolved(self):
        """Test Artcles"""
        url = reverse('articles')
        self.assertEquals(resolve(url).func.view_class, PostList)

    def test_post_detail_url_is_resolved(self):
        """Test Article Detail"""
        url = reverse('slug', args=['some-slug'])
        self.assertEquals(resolve(url).func.view_class, PostDetail)

    def test_post_like_url_is_resolved(self):
        """Test Likes"""
        url = reverse('like', args=['some-slug'])
        self.assertEquals(resolve(url).func.view_class, PostLike)
