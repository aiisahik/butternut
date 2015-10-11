from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
import ittakes2.account.api as AccountAPI
from models import Match
import datetime


class MatchResource(ModelResource):
    winner = fields.ForeignKey(AccountAPI.ProfileResource, 'winner', full=False)
    loser = fields.ForeignKey(AccountAPI.ProfileResource, 'loser', full=False)
    # winner_id = fields.IntegerProperty()
    class Meta:
        queryset = Match.objects.all()
        resource_name = 'match'
        list_allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True
        authorization= Authorization()

    def obj_create(self, bundle, **kwargs):
    	bundle.data['create_date'] = datetime.datetime.now()
    	result = super(MatchResource, self).obj_create(bundle, **kwargs)
    	match_result = result.obj.calc_result(save_rating=True, update_profiles=True)
    	
    	result.data['winner_last_name'] = result.obj.winner.last_name
    	result.data['winner_first_name'] = result.obj.winner.first_name
    	result.data['new_winner_elo'] = result.obj.winner.elo
    	result.data['new_winner_mu'] = result.obj.winner.mu
    	result.data['new_winner_sigma'] = result.obj.winner.sigma
    	result.data['loser_last_name'] = result.obj.loser.last_name
    	result.data['loser_first_name'] = result.obj.loser.first_name
    	result.data['new_loser_elo'] = result.obj.loser.elo
    	result.data['new_loser_mu'] = result.obj.loser.mu
    	result.data['new_loser_sigma'] = result.obj.loser.sigma
    	return result

    def dehydrate(self, bundle):
		bundle.data['winner_id'] = bundle.obj.winner_id
		bundle.data['loser_id'] = bundle.obj.loser_id
		return bundle