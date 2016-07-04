from leagues.models import Team, League
from leagues.utils import JSONView


class LeagueView(JSONView):
    def get(self, request, league_id):
        try:
			league = League.objects.get(id=league_id)
        except League.DoesNotExist:
            raise Http404()

        data = league.to_data()
        return data


class TeamView(JSONView):
    def get(self, request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            raise Http404()

        data = team.to_data()
        return data
