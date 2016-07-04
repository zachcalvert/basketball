from django.conf.urls import url

from leagues import views

urlpatterns = (
    url(r'^(?P<page_path>.+)/?$', views.WebPageWrapperView.as_view(), name='web_page_wrapper'),
    url(r'', views.LeaguesListView.as_view(), name='league_list'),
)