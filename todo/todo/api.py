from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie.constants import ALL,ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization,DjangoAuthorization
from tastypie.exceptions import Unauthorized
from django.contrib.auth.models import User
from todo_list.models import List,Task,Share
from tastypie import bundle
from itertools import chain
from django.conf.urls import url

# Authorization class for filtering data which doesnot belong to the user.
class UserAuthorization(DjangoAuthorization):

	def read_detail(self,object_list,bundle):
		return bundle.obj.user == bundle.request.user
	
	def read_list(self,object_list,bundle):
		object_list = object_list.filter(username=bundle.request.user.username,email=bundle.request.user.email) or None
		if object_list is None:
			return ["Either the credentials are wrong or user with the provided credentials does not exist."]
		return object_list

# Authorization class for filtering lists which doesnot belong to the user.
class ListAuthorization(DjangoAuthorization):

	def read_detail(self,object_list,bundle):
		# check if author
		if bundle.obj.author == bundle.request.user:
			return True
		# check if shared user
		valid_1 = Share.objects.get(listid__id=bundle.obj.id,user=bundle.request.user) or None
		if valid_1 is not None:
			return True
		return False

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
		# list1.extend(list2)
		object_list = list(chain(*object_list))
		return object_list

	def create_detail(self,object_list,bundle):
		return bundle.obj.author == bundle.request.user

	def create_list(self,object_list,bundle):
		print(object_list)
		return object_list

		
	def update_detail(self,object_list,bundle):
		print(object_list)
		return bundle.obj.author == bundle.request.user

	def delete_detail(self,object_list,bundle):
		print(object_list)
		return bundle.obj.author == bundle.request.user


class TaskAuthorization(DjangoAuthorization):

	def read_detail(self,object_list,bundle):
		# check if it is author
		if bundle.obj.listid.author == bundle.request.user:
			return True
		# check if it is shared list
		shared = Share.objects.filter(listid = bundle.obj.listid,user=bundle.request.user) or None
		if shared is not None:
			return True

		return False


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

	def create_deatil(self,object_list,bundle):
		# add logic on who can create tasks
		# check if user is author of the list
		ajkjbhbcj
		# print(bundle.obj)
		valid_1 = List.objects.get(id=bundle.obj.listid.id)
		if valid_1.user == bundle.request.user:
			return True
		# check if list is shared with user
		# valid_2 = List.object.get(id= bundle.obj.listid.id)
		valid_2 = Share.objects.get(listid=valid_1,user=bundle.request.user) or None
		if valid_2 is not None:
			return True
		return False


class SharedWithMeAuthorization(DjangoAuthorization):

	def read_list(self,object_list,bundle):
		object_list = object_list.filter(user=bundle.request.user)
		return object_list

class SharedByMeAuthorization(DjangoAuthorization):

	def read_list(self,object_list,bundle):
		object_list = object_list.filter(listid__author__id=bundle.request.user.id)
		return object_list

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name ='auth/user'
		excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
		allowed_methods = ['get']
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

	def prepend_urls(self):
				# print(resource_name)
		return [
			# url(r"^(?P<resource_name>%s)/(?P<pk>\d+)%s$" % (self._meta.resource_name,trailing_slash()), self.wrap_view('particular_id'), name='api_particular_list_id'),
			url(r"^(?P<resource_name>%s)/share/(?P<listid>\d+)/(?P<username>\w[\w/-]*)%s$" % (self._meta.resource_name,trailing_slash()), self.wrap_view('sharelist'), name='api_particular_list_share'),
			url(r"^(?P<resource_name>%s)/create/(?P<list_name>\w[\w/-]*)%s$" % (self._meta.resource_name,trailing_slash()), self.wrap_view('createlist'), name='api_create_list'),
		]

	# def particular_id(self,request,**kwargs):
		# # self.method_check(request,allowed=['get','post'])
		# self.is_authenticated(request)
		# # self.throttle_check(request)
		# # Do the query here:
		# # print("hello world")
		# try:
		# 	send_response = List.objects.get(id=kwargs['pk'],author=request.user)
		# 	send_response = {'author':send_response.author,'author_id':send_response.author.id,'date_posted':send_response.date_posted,'id':send_response.id,'list_name':send_response.list_name,'completed':send_response.completed,'last_modified':send_response.last_modified}
		# except List.DoesNotExist:
		# 	send_response={}
		# # print(kwargs)
		# return self.create_response(request,send_response)

	def sharelist(self,request,**kwargs):
		self.is_authenticated(request)
		# print(kwargs)
		# username exist or not
		try:
			check_username_validity = User.objects.get(username = kwargs['username'])
		except User.DoesNotExist:
			return self.create_response(request,{'error':'username entered doesnot exist'})
		# check if the entered list id is valid
		try:
			check_listid_valid = List.objects.get(id=kwargs['listid'])
		except List.DoesNotExist:
			return self.create_response(request,{'error':'entered listid doesnot exist'})
		# check is user is sending request to himself
		try:
			valid_request = List.objects.get(id=kwargs['listid'], author__username=kwargs['username'])
		except List.DoesNotExist:
			valid_request = None
		if valid_request is not None:
			return self.create_response(request,{'error':"cannot send owner's list to owner itself."})
		# Before sharing Authorize user from both list and share models
		try:
			valid_1 = List.objects.get(id=kwargs['listid'],author=request.user)
		except List.DoesNotExist:
			valid_1 = None
		try:
			valid_2 = Share.objects.get(listid__id=kwargs['listid'],user = request.user)
		except Share.DoesNotExist:
			valid_2 = None
		if valid_1 is None and valid_2 is None:
			return self.create_response(request,{'error':'you do not have access to the list with entered id.'})
		# check if list is already shred with the entered username or not
		try:
			valid_sharing = Share.objects.get(listid=kwargs['listid'],user__username=kwargs['username'])
		except Share.DoesNotExist:
			valid_sharing = None
		if valid_sharing is not None:
			return self.create_response(request,{'error':'list is already shared cannot be shared with the same user again.'})
		list_ref = List.objects.get(id=kwargs['listid'])
		user_ref = User.objects.get(username=kwargs['username'])
		ref_list_id = list_ref.id
		ref_user_id = user_ref.id
		sharing = Share(user=user_ref,listid=list_ref,shared_list_id=ref_list_id,sahred_user_id=ref_user_id)
		sharing.save()
		return self.create_response(request,{'status':'well done your list is shared successfully.'})

	def createlist(self,request,**kwargs):
		self.is_authenticated(request)
		# print(kwargs)
		try:
			q = List(author=request.user,list_name=kwargs['list_name'])
			q.save()
		except:
			return self.create_response(request,{'error':'cannot generate list.'})
		return self.create_response(request,{'status':'200','message':'list wtih provided name is generated successfully.'})



class TaskResource(ModelResource):
	_list = fields.ForeignKey(ListResource,'listid', full=True)
	# _user = fields.ForeignKey(UserResource,'user')
	class Meta:
		queryset = Task.objects.all()
		resource_name = 'tasks'
		filtering={
		'_list':ALL_WITH_RELATIONS,
		'id':ALL_WITH_RELATIONS,
		}
		authentication = ApiKeyAuthentication()
		authorization = TaskAuthorization()

	def prepend_urls(self):
		return [
		# url(r"^(?P<resource_name>%s)/(?P<pk>\d+)%s$" % (self._meta.resource_name,trailing_slash()), self.wrap_view('particular_id'), name='api_particular_list_id'),
		url(r"^(?P<resource_name>%s)/all%s$" % (self._meta.resource_name,trailing_slash()), self.wrap_view('alltasks'), name='api_all_id_tasks'),
		url(r"^(?P<resource_name>%s)/list/(?P<listid>\d+)%s$" % (self._meta.resource_name,trailing_slash()), self.wrap_view('listtasks'), name='api_all_id_tasks'),
		url(r"^(?P<resource_name>%s)/create/(?P<listid>\d+)/(?P<task_name>\w[\w/-]*)%s$" % (self._meta.resource_name,trailing_slash()), self.wrap_view('createtask'), name='api_all_id_tasks'),
		]

	# def particular_id(self,request,**kwargs):
	# 	# self.method_check(request,allowed=['get','post'])
	# 	self.is_authenticated(request)
	# 	# Do the query here
	# 	ids =[]
	# 	# find all the list ids from both shared and main list table
	# 	try:
	# 		list1 = List.objects.filter(author = request.user)
	# 	except List.DoesNotExist:
	# 		list1 = None
	# 	try:
	# 		list2 = Share.objects.filter(user=request.user)
	# 	except Share.DoesNotExist:
	# 		list2 = None

	# 	if list1 is not None:
	# 		for entry in list1:
	# 			ids.append(entry.id)
	# 	if list2 is not None:
	# 		for entry in list2:
	# 			ids.append(entry.listid.id)
	# 	try:
	# 		send_response = Task.objects.get(id = kwargs['pk'],listid__id__in=ids)
	# 		send_response = {'date_posted':send_response.date_posted,'id':send_response.id,'task':send_response.task,'completed':send_response.completed,'last_modified':send_response.last_modified,'list_name':send_response.listid.list_name,'list_id':send_response.listid.id}
	# 	except Task.DoesNotExist:
	# 		send_response = {'error':"You don't have access to that task id."}

	# 	return self.create_response(request,send_response)

	def alltasks(self,request,**kwargs):
		# self.method_check(request,allowed=['get','post'])
		self.is_authenticated(request)
		# Do the query here
		ids =[]
		# find all the list ids from both shared and main list table
		try:
			list1 = List.objects.filter(author = request.user)
		except List.DoesNotExist:
			list1 = None
		try:
			list2 = Share.objects.filter(user=request.user)
		except Share.DoesNotExist:
			list2 = None

		if list1 is not None:
			for entry in list1:
				ids.append(entry.id)
		if list2 is not None:
			for entry in list2:
				ids.append(entry.listid.id)
		if not ids:
			return self.create_response(request,{'error-message':'Their is no tasks available.'})

		output=[]
		all_tasks_details = Task.objects.filter(listid__id__in=ids)
		for send_response in all_tasks_details:
			data = {
			'date_posted':send_response.date_posted,'id':send_response.id,'task':send_response.task,
			'completed':send_response.completed,'last_modified':send_response.last_modified,
			'list_name':send_response.listid.list_name,'list_id':send_response.listid.id
			}
			output.append(data)

		return self.create_response(request,output)

	def listtasks(self,request,**kwargs):
		# self.method_check(request,allowed=['get','post'])
		self.is_authenticated(request)
		# Do the query here
		ids =[]
		# find whether user have the authority to access the list or not
		try:
			list1 = List.objects.get(id=kwargs['listid'],author = request.user)
		except List.DoesNotExist:
			list1 = None
		try:
			list2 = Share.objects.get(listid__id=kwargs['listid'],user=request.user)
		except Share.DoesNotExist:
			list2 = None
		# list id either doesnot exist or user don't have the authority
		if list1 is None and list2 is None:
			return self.create_response(request,{'error-message':"either the list id provided is not correct or you don't have permisiion to access the tasks in the list"})
		# user is valid and have authority to access the tasks.
		output=[]
		all_tasks_details = Task.objects.filter(listid__id=kwargs['listid'])
		for send_response in all_tasks_details:
			data = {
			'date_posted':send_response.date_posted,'id':send_response.id,'task':send_response.task,
			'completed':send_response.completed,'last_modified':send_response.last_modified,
			'list_name':send_response.listid.list_name,'list_id':send_response.listid.id
			}
			output.append(data)
		if not output:
			output = {'message':'Their is no task to be shown in the list.'}

		return self.create_response(request,output)

	def createtask(self,request,**kwargs):
		self.is_authenticated(request)
		# check if the id provided is correct or not
		print("hello world")
		try:
			list_id = List.objects.get(id=kwargs['listid'])
		except List.DoesNotExist:
			return self.create_response(request,{'error-message':'The task you are trying to add cannot be added as list with provided id doesnot exist.'})
		# check if the user have authority or not
		if list_id.author != request.user:
		# 	# check if list is shared with user
			try:
				valid_2 = Share.objects.get(listid=list_id,user=request.user)
			except Share.DoesNotExist:
				return self.create_response(request,{'error-message':"You don't have access to this list."})
		q = Task(listid=list_id,task=kwargs['task_name'])
		q.save()
		return self.create_response(request,{'status':'200','message':'task added to the list successfully'})



class SharedWithMeResource(ModelResource):
	_user = fields.ForeignKey(UserResource,'user',full=True)
	_list = fields.ForeignKey(ListResource,'listid',full=True)
	class Meta:
		queryset = Share.objects.all()
		resource_name = 'sharedwithme'
		allowed_methods = ['get']
		authentication = ApiKeyAuthentication()
		authorization = SharedWithMeAuthorization()

class SharedByMeResource(ModelResource):
	_user = fields.ForeignKey(UserResource,'user',full=True)
	_list = fields.ForeignKey(ListResource,'listid',full=True)
	class Meta:
		queryset = Share.objects.all()
		resource_name = 'sharedbyme'
		allowed_methods = ['get']
		authentication = ApiKeyAuthentication()
		authorization = SharedByMeAuthorization()

