from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
 
# Create your views here.
def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			# try catch is to check whether the user with provided email already exist or not.
			try:
				# form_username = form.cleaned_data.get('username')
				form_email = form.cleaned_data.get('email')
				exists = User.objects.get(email=form_email)
				# print("hello world ")
				print(form_email)
			except User.DoesNotExist:
				form.save()
				messages.success(request,f'Your Account has been created ! You can Login Now')
				return redirect('login')
			messages.error(request,'User with provided email already exist.')
			form = UserRegistrationForm()
			# return render(request,'users/register.html',{'form':form})
	else:
		form = UserRegistrationForm()
	return render(request,'users/register.html',{'form':form})


def email(request,list_id,user_name):
	subject = 'this is test mail'
	print(list_id)
	message = 'localhost:8000/task_home/'+list_id
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [user_name,]
	send_mail(subject,message,email_from,recipient_list)
	return redirect('home')

