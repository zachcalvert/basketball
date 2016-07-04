from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    url(r'api/', include('leagues.api_urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('leagues.urls')),		
]
