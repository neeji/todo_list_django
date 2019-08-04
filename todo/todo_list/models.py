from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

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
		return self.task + '|' + str(sel.completed)