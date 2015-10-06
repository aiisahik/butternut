from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class Profile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	mu = models.FloatField(null=True, blank=True)
	sigma = models.FloatField(null=True, blank=True)
	dob = models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		return "{0} - {1}".format(self.user.username, self.last_name)

	def get_matches(self):
		import datetime
		from ittakes2.matches.models import Match
		date_now = datetime.datetime.now()
		profile_matches = Match.objects.filter(
			Q(expire_date=None) | Q(expire_date__gt=date_now),
			Q(winner=self) | Q(loser=self)).order_by('create_date').all()
		return profile_matches

	def get_latest_match(self):
		import datetime
		from ittakes2.matches.models import Match
		date_now = datetime.datetime.now()
		latest_profile_match = Match.objects.filter(
			Q(expire_date=None) | Q(expire_date__gt=date_now),
			Q(winner=self) | Q(loser=self)).order_by('-create_date')[:1].first()		
		return latest_profile_match


# Create your models here.
