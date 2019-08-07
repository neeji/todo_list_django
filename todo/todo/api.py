from tastypie.resources import ModelResource
from tastypie.constants import ALL,ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization,DjangoAuthorization
from tastypie.exceptions import Unauthorized
from django.contrib.auth.models import User
from todo_list.models import List,Task,Share
from tastypie import bundle

class ListAuthorization(Authorization):
	def read_list(self, object_list, bundlle):
		import ipdb; ipdb.set_trace()
		return object_list.filter(author=bundle.request.user)

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name ='auth/user'
		excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
		allowed_methods = ['get']
		# authentication = BasicAuthentication()
		# authorization = DjangoAuthorization()
		filtering={
		'username':ALL,
		'id': ALL,
		}
		authentication = ApiKeyAuthentication()

class ListResource(ModelResource):
	author = fields.ForeignKey(UserResource,'author',full=True)
	class Meta:
		# authorization = DjangoAuthorization()
		queryset = List.objects.all()
		# fields=[full=True]
		# excludes = ['email', 'password', 'is_superuser']
		resource_name = 'lists'
		# allowed_methods = ['get']
		filtering = {
            'author':ALL_WITH_RELATIONS,
            'id':ALL,
        }
		authentication = ApiKeyAuthentication()
		authorization = ListAuthorization()

class TaskResource(ModelResource):
	_list = fields.ForeignKey(ListResource,'listid', full=True)
	# _user = fields.ForeignKey(UserResource,'user')
	class Meta:
		queryset = Task.objects.all()
		resource_name = 'tasks'
		filtering={
		'_list':ALL_WITH_RELATIONS,
		}
		authentication = ApiKeyAuthentication()

class SharedResource(ModelResource):
	class Meta:
		queryset = Share.objects.all()
		resource_name = 'shared'