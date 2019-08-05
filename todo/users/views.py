from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.core.mail import send_mail
from django.conf import settings
 
# Create your views here.
def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f'Your Account has been created ! You can Login Now')
			return redirect('login')
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

