from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from models import Profile


class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']


class ProfileResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	# id = fields.IntegerField(attribute='id')
	# fields = ['id', 'elo', 'mu', 'sigma', 'first_name', 'last_name']

	class Meta:
		queryset = Profile.objects.order_by('-elo').all()
		resource_name = 'profile'
		authorization= Authorization()

	def dehydrate(self, bundle):
		bundle.data['user_id'] = bundle.obj.user_id
		return bundle