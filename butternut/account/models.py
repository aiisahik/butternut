from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class Profile(models.Model):
	GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

	user = models.OneToOneField(User, primary_key=True)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)

	dob = models.DateTimeField(null=True, blank=True)
	gender = models.CharField(max_length=10, 
									choices=GENDER_CHOICES,
									default='F')
	gender_preference = models.CharField(max_length=10, 
									choices=GENDER_CHOICES,
									default='M')

	def __unicode__(self):
		return "{0} - {1}".format(self.user.username, self.last_name)

	def get_matches(self):
		import datetime
		from butternut.matches.models import Match
		date_now = datetime.datetime.now()
		profile_matches = Match.objects.filter(
			Q(expire_date=None) | Q(expire_date__gt=date_now),
			Q(winner=self) | Q(loser=self)).order_by('create_date').all()
		return profile_matches

	def get_latest_match(self):
		import datetime
		from butternut.matches.models import Match
		date_now = datetime.datetime.now()
		latest_profile_match = Match.objects.filter(
			Q(expire_date=None) | Q(expire_date__gt=date_now),
			Q(winner=self) | Q(loser=self)).order_by('-create_date')[:1].first()		
		return latest_profile_match


# Create your models here.
