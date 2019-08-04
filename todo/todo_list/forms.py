from django import forms
from .models import List,Task

class ListForm(forms.ModelForm):
	class Meta:
		model = List
		fields = ['list_name','completed']

class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['task','completed']