import json
from django.test import TestCase, Client

from leagues.models import League, Team
from players.models import Player

class TestAPIViews(TestCase):
	def setUp(self):
		for i in range(20):
			User.objects.create(username='user{}'.format(i), password='1234', email='{}@test.com'.format(i))

		self.league1 = League.objects.create(name="Test League One", manager=User.objects.first())
		self.league2 = League.objects.create(name="Test League Two", manager=User.objects.last())

		for i in range(20):
			if i %2 == 0:
				Team.objects.create(league=self.league2, name="team{}".format(i), owner=User.objects.get(id=i))
			else:
				Team.objects.create(league=self.league1, name="team{}".format(i), owner=User.objects.get(id=i))

		for i in range(200):
			player = Player.objects.create(name='Player {}'.format(i))
			team = Team.objects.order_by('?').first()
			team.players.add(player)

	def test_team_api_view(self):
		team = Team.objects.order_by('?').first()
		url = reverse('team', kwargs={'team_id': team.id})
		response = self.client.get(url)
        data = json.loads(response.content)

        # Test publisher
        self.assertEqual(
            {'name': team.name,
             'owner': team.owner.username,
             'record': team.record,
             'players': [{
				'id': player.id,
				'name': player.name,
				'position': player.position,
				'team': player.nba_team
			 } for player in team.players.all()]
			}, data)

		