"""Imports"""
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.


STATUS = ((0, 'Draft'), (1, 'Published'))


class Post(models.Model):
    """Post Model"""
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='article_like', blank=True)

    class Meta:
        """Created on order"""
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        """Artcle likes"""
        return self.likes.count()
