from . import views
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('articles/', views.PostList.as_view(), name='articles'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='article_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]
