from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tastypie.models import create_api_key

# Create your models here.

# class User(User, models.Model):
# 	name = models.CharField(null=True, max_length=32)
# 	class Meta:
# 		ordering = ('id',)

# 	def __str__(self):
# 		return self.name

models.signals.post_save.connect(create_api_key, sender=User)

class List(models.Model):
	list_name = models.CharField(max_length=200)
	completed = models.BooleanField(default=False)
	date_posted = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.list_name + ' | ' + str(self.completed)

class Task(models.Model):
	task = models.CharField(max_length=200)
	completed = models.BooleanField(default=False)
	date_posted = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	# listid = models.IntegerField(default=0)
	listid = models.ForeignKey(List,on_delete=models.CASCADE)

	def __str__(self):
		return self.task + '|' + str(self.completed)

class Share(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	listid = models.ForeignKey(List,on_delete=models.CASCADE)
	sahred_user_id = models.IntegerField()
	shared_list_id = models.IntegerField()

	def __str__(self):
		return str(self.sahred_user_id) + '|' + str(self.shared_list_id)