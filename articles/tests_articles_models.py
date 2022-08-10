"""Imports"""
from datetime import date
from django.test import TestCase
from articles.models import Post
from tests.tests_utils import TestUserUtils


class TestPost(TestCase):
    """Test post"""
    def setup(self):
        """Test post"""
        user = TestUserUtils.create_test_user('projectname', 'passw00rd')
        post = Post.objects.create(
            title='Biking under rain',
            slug='biking-under-rain',
            author=user,
            featured_image='default-image',
            excerpt='',
            updated_on=date.today(),
            content='I really like biking',
            created_on=date.today(),
            status=0,
            )
        return post

    # Test when a new post is created, but not published.
    def test_post_create(self):
        """Test post creation"""
        user = TestUserUtils.create_test_user('projectest', 'passw00rd')
        post = Post.objects.create(
                title='Biking',
                slug='biking',
                author=user,
                excerpt='',
                updated_on=date.today(),
                content='I really like biking',
                created_on=date.today(),
                status=0,
        )
        assert post.title == 'Biking'
        assert post.slug == 'biking'
        assert post.author.username == 'projectest'
        assert post.featured_image == 'default_image' # If no img is added
        assert post.excerpt == ''
        assert str(post.updated_on)[0:10] == str(date.today())
        assert post.content == 'I really like biking'
        assert str(post.created_on)[0:10] == str(date.today())
        assert post.published == 0
        assert post.status == None
        assert post.likes.count() == 0
        assert post.number_of_likes == '0'
        assert post.liked == False