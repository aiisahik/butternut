from django.db import models
from django.db.models.aggregates import Count
from random import randint
from ittakes2.account.models import Profile
from trueskill import Rating, quality_1vs1, rate_1vs1
import elo
import datetime

POSITION_CHOICES = (
    ('EAST', 'EAST'),
    ('WEST', 'WEST')
)

class MatchManager(models.Manager):
	def generate_random_match(self):
		profile_count = Profile.objects.count()
		random_index_1 = randint(0, profile_count - 1)
		random_index_2 = randint(0, profile_count - 2)
		winner = Profile.objects.all()[random_index_1]
		winner_score = 21
		loser = Profile.objects.exclude(user__id=winner.user_id)[random_index_2]
		loser_score = randint(10,19)
		winner_position = randint(0,1) and 'EAST' or 'WEST'
		loser_position = winner_position == 'EAST' and 'WEST' or 'EAST' 

		new_match = Match(winner=winner, loser=loser, winner_score=winner_score, loser_score=loser_score, winner_position=winner_position, loser_position=loser_position, create_date=datetime.datetime.now())
		return new_match
	
	def generate_random_matches(self, num):
		for i in [0] * num:
			new_match = self.generate_random_match()
			new_match.save()
			print new_match
			print "============================"
# from ittakes2.matches.models import *
# Match.objects.get_match()

class Match(models.Model):
	winner = models.ForeignKey(Profile, related_name="winners", related_query_name="winner")
	loser = models.ForeignKey(Profile, related_name="losers", related_query_name="loser")
	winner_score = models.SmallIntegerField(null=True, blank=True)
	loser_score = models.SmallIntegerField(null=True, blank=True)

	winner_mu =  models.FloatField(null=True, blank=True)
	winner_sigma =  models.FloatField(null=True, blank=True)
	winner_elo =  models.FloatField(null=True, blank=True)
	loser_mu =  models.FloatField(null=True, blank=True)
	loser_sigma =  models.FloatField(null=True, blank=True)
	loser_elo =  models.FloatField(null=True, blank=True)

	winner_position = models.CharField(max_length=4,choices=POSITION_CHOICES, null=True, blank=True)
	loser_position = models.CharField(max_length=4,choices=POSITION_CHOICES, null=True, blank=True)

	create_date = models.DateTimeField(auto_now=False)
	expire_date = models.DateTimeField(auto_now=False, null=True, blank=True)
	objects = MatchManager()
	
	def __unicode__(self):
		return "{0} beats {1}".format(self.winner.last_name, self.loser.last_name)

	def calc_result(self, existing_rankings={}, save_rating=False, update_profiles=False): 
		# match_winner = match.winner
		# match_loser = match.loser

		if existing_rankings and self.winner in existing_rankings and "trueskill" in existing_rankings[self.winner]:
			winner_trueskill_rating = existing_rankings[self.winner]["trueskill"]
		elif self.winner.mu and self.winner.sigma: 
			winner_trueskill_rating = Rating(mu=self.winner.mu, sigma=self.winner.sigma)
		else:
			winner_trueskill_rating = Rating()
			# print "initializing", self.winner 

		if existing_rankings and self.winner in existing_rankings and "elo" in existing_rankings[self.winner]:
			winner_elo_rating = existing_rankings[self.winner]["elo"]
		elif self.winner.elo: 
			winner_elo_rating = self.winner.elo
		else:
			winner_elo_rating = elo.INITIAL

		if existing_rankings and self.loser in existing_rankings and "trueskill" in existing_rankings[self.loser]:
			loser_trueskill_rating = existing_rankings[self.loser]["trueskill"]
		elif self.loser.mu and self.loser.sigma: 
			loser_trueskill_rating = Rating(mu=self.loser.mu, sigma=self.loser.sigma)
		else: 
			loser_trueskill_rating = Rating()
			print "initializing", self.loser
		
		if existing_rankings and self.loser in existing_rankings and "elo" in existing_rankings[self.loser]:
			loser_elo_rating = existing_rankings[self.loser]["elo"]
		elif self.loser.elo: 
			loser_elo_rating = self.loser.elo
		else:
			loser_elo_rating = elo.INITIAL

		if save_rating:
			self.winner_mu = winner_trueskill_rating.mu
			self.winner_sigma = winner_trueskill_rating.sigma
			self.winner_elo = winner_elo_rating
			self.loser_mu = loser_trueskill_rating.mu
			self.loser_sigma = loser_trueskill_rating.sigma
			self.loser_elo = loser_elo_rating
			self.save()



		new_winner_trueskill_rating, new_loser_trueskill_rating = rate_1vs1(winner_trueskill_rating, loser_trueskill_rating)

		elo_result = elo.rate_1vs1(winner_elo_rating, loser_elo_rating)
		new_winner_elo_rating = elo_result[0]
		new_loser_elo_rating = elo_result[1]

		print "{0} - {1} beats {2}".format(self.create_date, self.winner, self.loser)
		# print self.winner.last_name, "has new rating: ", winner_trueskill_rating.mu, "-->", new_winner_trueskill_rating.mu
		# print self.loser.last_name, "has new rating: ", loser_trueskill_rating.mu, "-->", new_loser_trueskill_rating.mu
		print self.winner.last_name, "has new rating: ", winner_elo_rating , "-->", new_winner_elo_rating
		print self.loser.last_name, "has new rating: ", loser_elo_rating , "-->", new_loser_elo_rating
		print "============================"
		existing_rankings.setdefault(self.winner, {})
		existing_rankings.setdefault(self.loser, {})
		existing_rankings[self.winner]['trueskill'] = new_winner_trueskill_rating
		existing_rankings[self.loser]['trueskill'] = new_loser_trueskill_rating
		existing_rankings[self.winner]['elo'] = new_winner_elo_rating
		existing_rankings[self.loser]['elo'] = new_loser_elo_rating
		
		if update_profiles:
			self.winner.elo = new_winner_elo_rating
			self.winner.mu = new_winner_trueskill_rating.mu
			self.winner.sigma = new_winner_trueskill_rating.sigma
			self.winner.save()
			self.loser.elo = new_loser_elo_rating
			self.loser.mu = new_loser_trueskill_rating.mu
			self.loser.sigma = new_loser_trueskill_rating.sigma
			self.loser.save()

		return existing_rankings
# Create your models here.

def calc_all_rankings(save_rating=True):
	player_rankings = {}
	matches = Match.objects.order_by('create_date').all()
	for match in matches: 
		player_rankings = match.calc_result(existing_rankings=player_rankings,save_rating=True)
	print "New Rankings:"
	for player, ratings in player_rankings.iteritems():
		for rating_type, rating in ratings.iteritems():
			print player, rating_type, rating
		if save_rating:
			player.mu = ratings['trueskill'].mu
			player.sigma = ratings['trueskill'].sigma
			player.elo = ratings['elo']
			player.save()

	


