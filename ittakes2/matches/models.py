from django.db import models
from django.db.models.aggregates import Count
from random import randint
from ittakes2.account.models import Profile
from trueskill import Rating, quality_1vs1, rate_1vs1

class MatchManager(models.Manager):
	def generate_random_match(self):
		profile_count = Profile.objects.count()
		random_index_1 = randint(0, profile_count - 1)
		random_index_2 = randint(0, profile_count - 2)
		winner = Profile.objects.all()[random_index_1]
		winner_score = 21
		loser = Profile.objects.exclude(user__id=winner.user_id)[random_index_2]
		loser_score = randint(10,19)
		new_match = Match(winner=winner, loser=loser, winner_score=winner_score, loser_score=loser_score)
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
	loser_mu =  models.FloatField(null=True, blank=True)
	loser_sigma =  models.FloatField(null=True, blank=True)

	create_date = models.DateTimeField(auto_now=True)
	expire_date = models.DateTimeField(auto_now=False, null=True, blank=True)
	objects = MatchManager()
	
	def __unicode__(self):
		return "{0} beats {1}".format(self.winner.last_name, self.loser.last_name)

	def calc_result(self, existing_rankings=None, save_rating=False): 
		# match_winner = match.winner
		# match_loser = match.loser

		if existing_rankings and self.winner in existing_rankings:
			winner_rating = existing_rankings[self.winner]
		elif self.winner.mu and self.winner.sigma: 
			winner_rating = Rating(mu=self.winner.mu, sigma=self.winner.sigma)
		else:
			winner_rating = Rating()
			print "initializing", self.winner 

		if existing_rankings and self.loser in existing_rankings:
			loser_rating = existing_rankings[self.loser]
		elif self.loser.mu and self.loser.sigma: 
			loser_rating = Rating(mu=self.loser.mu, sigma=self.loser.sigma)
		else: 
			loser_rating = Rating()
			print "initializing", self.loser
		
		if save_rating:
			self.winner_mu = winner_rating.mu
			self.winner_sigma = winner_rating.sigma
			self.loser_mu = loser_rating.mu
			self.loser_sigma = loser_rating.sigma
			self.save()
		
		new_winner_rating, new_loser_rating = rate_1vs1(winner_rating, loser_rating)
		print "{0} - {1} beats {2}".format(self.create_date, self.winner, self.loser)
		print self.winner.last_name, "has new rating: ", winner_rating.mu, "-->", new_winner_rating.mu
		print self.loser.last_name, "has new rating: ", loser_rating.mu, "-->", new_loser_rating.mu
		print "============================"
		existing_rankings[self.winner] = new_winner_rating
		existing_rankings[self.loser] = new_loser_rating

		return existing_rankings
# Create your models here.



def calc_all_rankings(save_rating=True):
	player_rankings = {}
	matches = Match.objects.order_by('create_date').all()
	for match in matches: 
		player_rankings = match.calc_result(existing_rankings=player_rankings,save_rating=True)
	print "New Rankings:"
	for player, rating in player_rankings.iteritems():
		print player, rating.mu, rating.sigma
		if save_rating:
			player.mu = rating.mu
			player.sigma = rating.sigma
			player.save()

	


