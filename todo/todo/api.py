from tastypie.resources import ModelResource
from tastypie.constants import ALL,ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization,DjangoAuthorization
from tastypie.exceptions import Unauthorized
from django.contrib.auth.models import User
from todo_list.models import List,Task,Share
from tastypie import bundle
from itertools import chain

# Authorization class for filtering data which doesnot belong to the user.
class UserAuthorization(DjangoAuthorization):
	def read_list(self,object_list,bundle):
		return object_list.filter(username=bundle.request.user.username,email=bundle.request.user.email)

# Authorization class for filtering lists which doesnot belong to the user.
class ListAuthorization(DjangoAuthorization):
	def read_list(self,object_list,bundle):
		list1 = object_list.filter(author__id=bundle.request.user.id)
		# for adding shared lists of the user to t he returned data.
		shared_list = Share.objects.filter(user=bundle.request.user) or None
		if shared_list is None:
			object_list = list1
			return object_list	

		# If their is a shared list for the user then retrieve that list
		ids=[]
		for list_ids in shared_list:
			# print(ids.listid)
			ids.append(list_ids.listid.id) 

		list2 = object_list.filter(id__in=ids)
		"""
		chaining two list to return a single list to the api combining all the data of the first and the seond list.
		"""
		object_list = [list1,list2]
		object_list = list(chain(*object_list))
		return object_list

class TaskAuthorization(DjangoAuthorization):
	
	def read_list(self,object_list,bundle):
		# test = Share.objects.filter(user=bundle.request.user)
		# list1 = object_list.filter(listid)
		lists_owned = List.objects.filter(author=bundle.request.user) or None
		lists_shared = Share.objects.filter(user=bundle.request.user) or None

		if lists_owned is None and lists_shared is None:
			return []
		elif lists_shared is None and lists_owned is not None:
			ids=[]
			for owned in lists_owned:
				ids.append(owned.id)
			list1 = object_list.filter(listid__id__in=ids)
			object_list = list1
			return object_list
		elif lists_owned is None and lists_shared is not None:
			ids=[]
			for shared in lists_shared:
				ids.append(shared.listid.id)
			list1 = object_list.filter(listid__id__in=ids)
			object_list = list1
			return object_list
		else:
			ids = []
			for owned in lists_owned:
				ids.append(owned.id)
			for shared in lists_shared:
				ids.append(shared.listid.id)
			list1 = object_list.filter(listid__id__in=ids)
			object_list=list1
			return object_list

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
		authorization = UserAuthorization()

	# def login():


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
		authorization = TaskAuthorization()

class SharedResource(ModelResource):
	class Meta:
		queryset = Share.objects.all()
		resource_name = 'shared'