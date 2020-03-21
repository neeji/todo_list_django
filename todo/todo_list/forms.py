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

# incorrect way as their is no model class in it
# class ShareForm(forms.ModelForm):
# 	class Meta:
# 		fields = ['email_address']

class ShareForm(forms.Form):
	email = forms.CharField(max_length=100,label='email')