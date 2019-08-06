from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import List, Task, Share
from .forms import ListForm,TaskForm,ShareForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
	# return render(request,"home.html",{})
	if request.method == 'POST':
		form = ListForm(request.POST or None)

		if form.is_valid():
			# for adding user id along with the task we need user id
			form.instance.author = request.user
			form.save()
			# all_tasks = List.objects.all()
			messages.success(request,("List created Successfully..."))
			return redirect("home")
	else:
		# print(request.user.id)
		if(request.user.is_authenticated):
			all_lists = List.objects.filter(author=request.user.id)
			print(all_lists)
			shared_lists = Share.objects.filter(user=request.user)
			print(shared_lists)
			return render(request,'home.html',{'all_lists':all_lists,'shared_lists':shared_lists})
		else:
			return redirect('login')

@login_required
def task_home(request,list_id):
	# return render(request,"home.html",{})
	if request.method == 'POST':
		form = TaskForm(request.POST or None)

		if form.is_valid():
			# for adding user id along with the task we need user id
			listid = List.objects.get(pk=list_id)
			form.instance.listid = listid
			form.save()
			messages.success(request,("Task added to list Successfully..."))
			return redirect("task_home",list_id)
	else:
		# print(request.user.id)
		all_tasks=''

		try:
			user_id = request.user.id
			# for authenticating users
			try:
				valid_user_1 = List.objects.get(id=list_id,author=request.user)
			except List.DoesNotExist:
				valid_user_1=None
			try: 
				valid_user_2 = Share.objects.get(shared_list_id=list_id,sahred_user_id=request.user.id)
			except Share.DoesNotExist:
				valid_user_2=None
			# print(str(valid_user_1)+' '+str(valid_user_2))
			# print(list_id)
			if(valid_user_1 is None and valid_user_2 is None):
				return redirect("home")
			lsit = List.objects.get(pk=list_id)
			all_tasks = Task.objects.filter(listid=list_id)
		except List.DoesNotExist:
			return redirect("home")

		return render(request,'task_home.html',{'all_tasks':all_tasks})

def delete_list(request,list_id):
	# authenticate user first
	if(not request.user.is_authenticated):
		messages.error(request,"Please Sign In first if already registered otherwise register to our site.")
		return redirect('home')
	# check if list_id is correct or not
	try:
		valid_1 = List.objects.get(pk=list_id)
	except ListDoesNotExist:
		messages.error(request,"list you are trying to delete does not exist.")
		return redirect('home')
	# check authority of the user to delete list
	if valid_1.author != request.user:
		messages.error(request,"You don't have permission to do the following task.")
		return redirect('home')
	# if user is authenticated and authorised then continue to delete list.
	list_to_delete = List.objects.get(pk=list_id)
	list_to_delete.delete()
	messages.success(request,"List has been deleted successfully...")
	return redirect("home")

def delete(request,_id):
	# check authentication
	if(not request.user.is_authenticated):
		messages.error(request,'Please Sign In first.')
		return redirect('home')
	# check if task id is correct or not:
	try:
		task = Task.objects.get(pk=_id)
	except Task.DoesNotExist:
		messages.error(request,'Task you are trying to delete does not exist.')
		return redirect('home')
	# check authorization
	list_id = task.listid.id
	valid_check_1 = List.objects.get(pk=list_id)
	if valid_check_1.author != request.user:
		try:
			valid_check_2 = Share.objects.get(listid=list_id,user=request.user)
		except Share.DoesNotExist:
			messages.error(request,'You dont have permission for the applied task.')
			return redirect('home')
	task.delete()
	messages.success(request,"task has been deleted successfully...")
	return redirect("task_home",list_id)

def cross_off(request,_id):
	# check authentication
	if(not request.user.is_authenticated):
		messages.error(request,'Please Sign In first.')
		return redirect('home')
	# check if task id is correct or not:
	try:
		task = Task.objects.get(pk=_id)
	except Task.DoesNotExist:
		messages.error(request,'Task you are trying to mark done does not exist.')
		return redirect('home')
	# check authorization
	list_id = task.listid.id
	valid_check_1 = List.objects.get(pk=list_id)
	if valid_check_1.author != request.user:
		try:
			valid_check_2 = Share.objects.get(listid=list_id,user=request.user)
		except Share.DoesNotExist:
			messages.error(request,'You dont have permission for the applied task.')
			return redirect('home')
	task.completed = True
	task.save()
	return redirect("task_home",list_id)

def uncross(request,_id):
	# check authentication
	if(not request.user.is_authenticated):
		messages.error(request,'Please Sign In first.')
		return redirect('home')
	# check if task id is correct or not:
	try:
		task = Task.objects.get(pk=_id)
	except Task.DoesNotExist:
		messages.error(request,'Task you are trying to mark undone does not exist.')
		return redirect('home')
	# check authorization
	list_id = task.listid.id
	valid_check_1 = List.objects.get(pk=list_id)
	if valid_check_1.author != request.user:
		try:
			valid_check_2 = Share.objects.get(listid=list_id,user=request.user)
		except Share.DoesNotExist:
			messages.error(request,'You dont have permission for the applied task.')
			return redirect('home')
	task.completed = False
	task.save()
	return redirect("task_home",list_id)

def edit(request,_id):
	# check authentication
	if(not request.user.is_authenticated):
		messages.error(request,'Please Sign In first.')
		return redirect('home')
	# print(_id)
	# check if task id is correct or not:
	try:
		task = Task.objects.get(pk=_id)
	except Task.DoesNotExist:
		messages.error(request,'Task you are trying to edit does not exist.')
		return redirect('home')
	#check if the user have the authority to edit task or not 
	list_id = task.listid.id
	valid_check_1 = List.objects.get(pk=list_id)
	if valid_check_1.author != request.user:
		try:
			valid_check_2 = Share.objects.get(listid=list_id,user=request.user)
		except Share.DoesNotExist:
			messages.error(request,'You dont have permission for the applied task.')
			return redirect('home')
	if request.method=='POST':
		form = TaskForm(request.POST or None, instance=task)
		if form.is_valid():
			form.save()
			messages.success(request,('task has been edited successfully...'))
			return redirect('task_home',list_id)
	else:
		task = Task.objects.get(pk=_id)
		return render(request,'edit.html',{'task':task})

def share(request,list_id):
	# print(list_id)
	list_share=''
	user_sharing=''
	form = ShareForm()
	# if request.method=='POST':
	# 	list_share = List.objects.get(pk=list_id)
	# 	# print(list_share)
	# 	form = ShareForm(request.POST or None)
	# 	if form.is_valid():
	# 		# cd = form.cleaned_data
	# 		username = form.cleaned_data['email']
	# 		try:
	# 			user_sharing = User.objects.get(email=username)
	# 			# print(user_sharing)
	# 			try:
	# 				validate = Share.objects.get(sahred_user_id=user_sharing.id,shared_list_id=list_id)
	# 			except Share.DoesNotExist:
	# 				data = Share(user=user_sharing,listid=list_share,shared_list_id=list_id,sahred_user_id=user_sharing.id)
	# 				data.save()
	# 				messages.success(request,"Your list is shared successfully.")
	# 				# return redirect("home")
	# 				return redirect('email',list_id,username)
	# 			messages.error(request,'list already shared with the provided user email.')
	# 			return redirect("home")
	# 		except User.DoesNotExist:
	# 			messages.error(request,'email enterd is not valid or any user with the provided email doesnot exist.')
	# 			return render(request,'share.html',list_id)
	# 		# print(username)
	# 	else:
	# 		message.error(request,"some error occured please try again later.")
	# 		return redirect("home")
	# else:
	# 	return render(request,'share.html')

	if request.method!='POST':
		return render(request,'share.html')
		
	list_share = List.objects.get(pk=list_id)
	# print(list_share)
	form = ShareForm(request.POST or None)
	if not form.is_valid():
		message.error(request,"some error occured please try again later.")
		return redirect("home")

	# cd = form.cleaned_data
	username = form.cleaned_data['email']
	try:
		user_sharing = User.objects.get(email=username)
		# print(user_sharing)
		try:
			validate = Share.objects.get(user_id=user_sharing.id,listid_id=list_id)
			validate = Share.objects.get(user=user_sharing,listid_id=list_id)
			validate = Share.objects.get(user=user_sharing,listid=list_id)
		except Share.DoesNotExist:
			data = Share(user=user_sharing,listid=list_share,shared_list_id=list_id,sahred_user_id=user_sharing.id)
			data.save()
			messages.success(request,"Your list is shared successfully.")
			# return redirect("home")
			return redirect('email',list_id,username)

		messages.error(request,'list already shared with the provided user email.')
		return redirect("home")
	except User.DoesNotExist:
		messages.error(request,'email enterd is not valid or any user with the provided email doesnot exist.')
		return redirect('share',list_id)


