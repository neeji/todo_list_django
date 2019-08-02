from django.db import models

# Create your models here.

class List(models.Model):
	task = models.CharField(max_length=200)
	completed = models.BooleanField(default=False)

	def __str__(self):
		return self.task + ' | ' + str(self.completed)