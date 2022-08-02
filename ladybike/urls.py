"""ladybike URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403, handler404, handler500
from booking import views


urlpatterns = [
    path('', include('website.urls'), name='website_urls'),
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls), # Django admin route
    path('articles/', include('articles.urls'), name='articles-urls'),
    path('summernote/', include('django_summernote.urls')),
    path('classes', views.classes_urls),
    path('booking/', include(
        'booking.urls'), name='booking_urls'),
    path("accounts/", include("allauth.urls")),
]

handler404 = 'website.views.error_403'
handler404 = 'website.views.error_404'
handler500 = 'website.views.error_500'


