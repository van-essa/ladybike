from . import views
from django.urls import path, include
from django.contrib import admin
from django.conf.urls import handler400, handler500

urlpatterns = [
    path('', include('website.urls'), name='website_urls'),
    path('admin/', admin.site.urls),
    path('articles/', views.PostList.as_view(), name='articles'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='article_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('booking/', include(
        'booking.urls'), name='booking_urls'),
    path('accounts/', include('allauth.urls')),
]

handler404 = 'website.views.error_404'
handler500 = 'website.views.error_500'