from django.conf.urls import url

from leagues import views

urlpatterns = (
    url(r'^teams/(?P<team_id>\d+).json$', views.TeamView.as_view(), name='team'),
)