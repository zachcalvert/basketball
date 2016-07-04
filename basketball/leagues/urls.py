from django.conf.urls import url

from leagues import views

urlpatterns = (
    url(r'^league/(?P<league_id>\d+).json$', views.LeagueView.as_view(), name='team'),
    url(r'^teams/(?P<team_id>\d+).json$', views.TeamView.as_view(), name='team'),
)