from django.conf.urls import url

from leagues import views

urlpatterns = (
	url(r'', views.LeaguesListView.as_view(), name='leagues_list'),
    url(r'^league/(?P<league_id>\d+).json$', views.LeagueView.as_view(), name='league'),
	url(r'^league/(?P<league_id>\d+)/team/(?P<team_id>\d+).json$', views.TeamView.as_view(), name='team'),
    url(r'^league/(?P<league_id>\d+)/free_agents.json', views.TeamView.as_view(), name='free_agents'),
)