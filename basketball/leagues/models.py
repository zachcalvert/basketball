from __future__ import division
from django.db import models
from datetime import datetime, date, timedelta
from django.db.models import Q, Max
from django.contrib.auth.models import User


class League(models.Model):
	name = models.CharField(max_length=30)
	owner = models.ForeignKey(User)
	is_dynasty = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name


class Team(models.Model):
	league = models.ForeignKey(League)
	first_name = models.CharField(max_length=15, default='Team')
	last_name = models.CharField(max_length=15, default='Name')
	owner = models.ForeignKey(User, null=True)
	wins = models.IntegerField(default=0)
	losses = models.IntegerField(default=0)
	ties = models.IntegerField(default=0)

	class Meta:
		ordering = ['-wins', 'losses']

	def __unicode__(self):
		return "{0} {1}".format(self.first_name, self.last_name)

	@property
	def record(self):
		return "{0}-{1}-{2}".format(self.wins, self.losses, self.ties)

