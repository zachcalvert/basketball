from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class League(models.Model):
	name = models.CharField(max_length=30)
	manager = models.ForeignKey(User)
	is_dynasty = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

	def to_data(self, roster_data=False):
		data = {
			'name': self.name,
			'manager': self.manager.username,
			'is_dynasty': self.is_dynasty,
			'teams': [{
				'name': team.name,
				'owner': team.owner.username,
				'record': team.record
			} for team in self.teams.all()]
		}

		if roster_data:
			data['teams'] = [{
				'name': team.name,
				'owner': team.owner,
				'record': team.record,
				'players': [{
					'name': player.name,
					'position': player.position,
					'team': player.nba_team
				} for player in team.players.all()]

			} for team in self.teams.all()]

		return data


class Team(models.Model):
	league = models.ForeignKey(League, related_name='teams')
	name = models.CharField(max_length=30, default='Team')
	owner = models.ForeignKey(User, null=True)
	wins = models.IntegerField(default=0)
	losses = models.IntegerField(default=0)
	ties = models.IntegerField(default=0)
	players = models.ManyToManyField('players.Player', blank=True, related_name='teams')

	class Meta:
		ordering = ['-wins', 'losses']

	def __unicode__(self):
		return self.name

	@property
	def record(self):
		return "{0}-{1}-{2}".format(self.wins, self.losses, self.ties)

	def to_data(self):
		data = {
			'name': self.name,
			'owner': self.owner.username,
			'record': self.record,
			'players': [{
				'id': player.id,
				'name': player.name,
				'position': player.position,
				'team': player.nba_team
			} for player in self.players.all()]
		}

		return data

	def clean(self):
		for player in self.players.all():
			if Team.objects.filter(league=self.league).exclude(id=self.pk).filter(players__name=player.name):
				raise IntegrityError('%s is already on a team in this league: %s' % (player.name, self.name))

