from django.db import models
from django.db.models.aggregates import Count
from random import randint
from butternut.account.models import Profile
from trueskill import Rating, quality_1vs1, rate_1vs1
import elo
import datetime
from django.utils import timezone

POSITION_CHOICES = (
    ('EAST', 'EAST'),
    ('WEST', 'WEST')
)

class Player(models.Model):
	judge = models.ForeignKey(Profile, related_name="player_judges", related_query_name="player_judge")
	target = models.ForeignKey(Profile, related_name="target", related_query_name="target")
	mu = models.FloatField(null=True, blank=True)
	sigma = models.FloatField(null=True, blank=True)
	elo = models.FloatField(null=True, blank=True)
	update_date = models.DateTimeField(auto_now=False)
	rank = models.SmallIntegerField(null=True, blank=True)

	def __unicode__(self):
		return "{0} {1}: {2} {3} has mu: {4}, sigma: {5}".format(self.judge.first_name, self.judge.last_name, self.target.first_name, self.target.last_name, self.mu, self.sigma)

class MatchManager(models.Manager):
	
	def generate_random_match(self, judge):

		profile_count = Profile.objects.filter(gender=judge.gender_preference).count()
		random_index_1 = randint(0, profile_count - 1)
		random_index_2 = randint(0, profile_count - 2)
		winner = Profile.objects.filter(gender=judge.gender_preference)[random_index_1]
		loser = Profile.objects.filter(gender=judge.gender_preference).exclude(user__id=winner.user_id)[random_index_2]

		new_match = Match(winner=winner, loser=loser, judge=judge)
		return new_match
	
	def generate_random_matches(self, judge, num):
		for i in [0] * num:
			new_match = self.generate_random_match(judge=judge)
			new_match.save()
			winningPlayer, losingPlayer = new_match.get_players()
			winningPlayer.save()
			losingPlayer.save()
			print new_match
			print "winner: ", winningPlayer
			print "loser: ", losingPlayer
			print "============================"

class Match(models.Model):
	judge = models.ForeignKey(Profile, related_name="judges", related_query_name="judge", null=True, blank=True)
	winner = models.ForeignKey(Profile, related_name="winners", related_query_name="winner")
	loser = models.ForeignKey(Profile, related_name="losers", related_query_name="loser")
	
	create_date = models.DateTimeField(auto_now=True)
	expire_date = models.DateTimeField(auto_now=False, null=True, blank=True)
	objects = MatchManager()
	
	def __unicode__(self):
		return "{0} {1}: {2} {3} def. {4} {5}".format(self.judge.first_name, self.judge.last_name, self.winner.first_name, self.winner.last_name, self.loser.first_name, self.loser.last_name)

	def get_players(self): 

		date_now = timezone.now()
		winningPlayerQuery = Player.objects.filter(judge=self.judge, target=self.winner)
		if winningPlayerQuery.exists():
			winningPlayer = winningPlayerQuery[0]
			winningPlayerTrueskillExistingRating = Rating(mu=winningPlayer.mu, sigma=winningPlayer.sigma)
		else: 
			winningPlayer = Player(judge=self.judge, target=self.winner, update_date=date_now)
			winningPlayerTrueskillExistingRating = Rating()

		losingPlayerQuery = Player.objects.filter(judge=self.judge, target=self.winner)
		if losingPlayerQuery.exists():
			losingPlayer = losingPlayerQuery[0]
			losingPlayerTrueskillExistingRating = Rating(mu=losingPlayer.mu, sigma=losingPlayer.sigma)
		else: 
			losingPlayer = Player(judge=self.judge, target=self.loser, update_date=date_now)
			losingPlayerTrueskillExistingRating = Rating()

		winningPlayerTrueskillUpdatedRating, losingPlayerTrueskillUpdatedRating = rate_1vs1(winningPlayerTrueskillExistingRating, losingPlayerTrueskillExistingRating)
		
		winningPlayer.mu = winningPlayerTrueskillUpdatedRating.mu
		winningPlayer.sigma = winningPlayerTrueskillUpdatedRating.sigma
		# winningPlayer.save()

		losingPlayer.mu = losingPlayerTrueskillUpdatedRating.mu
		losingPlayer.sigma = losingPlayerTrueskillUpdatedRating.sigma
		# losingPlayer.save()

		return winningPlayer, losingPlayer

	# def calc_result(self, existing_rankings={}, save_rating=False, update_profiles=False): 
	# 	# match_winner = match.winner
	# 	# match_loser = match.loser

	# 	if existing_rankings and self.winner in existing_rankings and "trueskill" in existing_rankings[self.winner]:
	# 		winner_trueskill_rating = existing_rankings[self.winner]["trueskill"]
	# 	elif self.winner.mu and self.winner.sigma: 
	# 		winner_trueskill_rating = Rating(mu=self.winner.mu, sigma=self.winner.sigma)
	# 	else:
	# 		winner_trueskill_rating = Rating()
	# 		# print "initializing", self.winner 

	# 	if existing_rankings and self.winner in existing_rankings and "elo" in existing_rankings[self.winner]:
	# 		winner_elo_rating = existing_rankings[self.winner]["elo"]
	# 	elif self.winner.elo: 
	# 		winner_elo_rating = self.winner.elo
	# 	else:
	# 		winner_elo_rating = elo.INITIAL

	# 	if existing_rankings and self.loser in existing_rankings and "trueskill" in existing_rankings[self.loser]:
	# 		loser_trueskill_rating = existing_rankings[self.loser]["trueskill"]
	# 	elif self.loser.mu and self.loser.sigma: 
	# 		loser_trueskill_rating = Rating(mu=self.loser.mu, sigma=self.loser.sigma)
	# 	else: 
	# 		loser_trueskill_rating = Rating()
	# 		print "initializing", self.loser
		
	# 	if existing_rankings and self.loser in existing_rankings and "elo" in existing_rankings[self.loser]:
	# 		loser_elo_rating = existing_rankings[self.loser]["elo"]
	# 	elif self.loser.elo: 
	# 		loser_elo_rating = self.loser.elo
	# 	else:
	# 		loser_elo_rating = elo.INITIAL

	# 	if save_rating:
	# 		self.winner_mu = winner_trueskill_rating.mu
	# 		self.winner_sigma = winner_trueskill_rating.sigma
	# 		self.winner_elo = winner_elo_rating
	# 		self.loser_mu = loser_trueskill_rating.mu
	# 		self.loser_sigma = loser_trueskill_rating.sigma
	# 		self.loser_elo = loser_elo_rating
	# 		self.save()



		# new_winner_trueskill_rating, new_loser_trueskill_rating = rate_1vs1(winner_trueskill_rating, loser_trueskill_rating)

		# elo_result = elo.rate_1vs1(winner_elo_rating, loser_elo_rating)
		# new_winner_elo_rating = elo_result[0]
		# new_loser_elo_rating = elo_result[1]

		# print "{0} - {1} beats {2}".format(self.create_date, self.winner, self.loser)
		# # print self.winner.last_name, "has new rating: ", winner_trueskill_rating.mu, "-->", new_winner_trueskill_rating.mu
		# # print self.loser.last_name, "has new rating: ", loser_trueskill_rating.mu, "-->", new_loser_trueskill_rating.mu
		# print self.winner.last_name, "has new rating: ", winner_elo_rating , "-->", new_winner_elo_rating
		# print self.loser.last_name, "has new rating: ", loser_elo_rating , "-->", new_loser_elo_rating
		# print "============================"
		# existing_rankings.setdefault(self.winner, {})
		# existing_rankings.setdefault(self.loser, {})
		# existing_rankings[self.winner]['trueskill'] = new_winner_trueskill_rating
		# existing_rankings[self.loser]['trueskill'] = new_loser_trueskill_rating
		# existing_rankings[self.winner]['elo'] = new_winner_elo_rating
		# existing_rankings[self.loser]['elo'] = new_loser_elo_rating
		
		# if update_profiles:
		# 	self.winner.elo = new_winner_elo_rating
		# 	self.winner.mu = new_winner_trueskill_rating.mu
		# 	self.winner.sigma = new_winner_trueskill_rating.sigma
		# 	self.winner.save()
		# 	self.loser.elo = new_loser_elo_rating
		# 	self.loser.mu = new_loser_trueskill_rating.mu
		# 	self.loser.sigma = new_loser_trueskill_rating.sigma
		# 	self.loser.save()

		# return existing_rankings
# Create your models here.

def calc_all_rankings(save_rating=True):
	player_rankings = dict([ (profile, {'trueskill': Rating(), 'elo': elo.INITIAL}) for profile in Profile.objects.all()])
	print 'player_rankings', player_rankings
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

	


