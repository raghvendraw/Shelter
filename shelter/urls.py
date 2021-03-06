"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from settings import *
from master.views import slummap, city_wise_map
admin.autodiscover()

base64_pattern = r'^city::(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?'
urlpatterns = [
    url(r'^$',slummap, name='slummap'),
    url(r'^(?P<key>{})$'.format(base64_pattern), city_wise_map, name="city_map"),
    url(r'^(?P<key>{})/(?P<slumname>.*)$'.format(base64_pattern), city_wise_map, name="city_mapp"),
    url(r'^admin/', include('master.urls')),
    url(r'^component/', include('component.urls')),
    url(r'^sponsor/', include('sponsor.urls')),
    url(r'^mastersheet/', include('mastersheet.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = settings.ADMIN_SITE_HEADER
