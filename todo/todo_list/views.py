from django.shortcuts import render,redirect
from .models import List, Task
from .forms import ListForm,TaskForm
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
			# return render(request,'home.html',{'all_tasks':all_tasks})
	else:
		# print(request.user.id)
		all_lists = List.objects.filter(author=request.user.id)
		return render(request,'home.html',{'all_lists':all_lists})

@login_required
def task_home(request,_id):
	# return render(request,"home.html",{})
	if request.method == 'POST':
		form = TaskForm(request.POST or None)

		if form.is_valid():
			# for adding user id along with the task we need user id
			listid = List.objects.get(pk=_id)
			form.instance.listid = listid
			form.save()
			# all_tasks = List.objects.all()
			messages.success(request,("Task added to list Successfully..."))
			return redirect("task_home",_id)
			# return render(request,'home.html',{'all_tasks':all_tasks})
	else:
		# print(request.user.id)
		all_tasks = Task.objects.filter(listid=_id)
		return render(request,'task_home.html',{'all_tasks':all_tasks})

def delete(request,list_id):
	task = List.objects.get(pk=list_id)
	task.delete()
	messages.success(request,"task has been deleted successfully...")
	return redirect("home")

def cross_off(request,list_id):
	task = List.objects.get(pk = list_id)
	task.completed = True
	task.save()
	return redirect("home")

def uncross(request,list_id):
	task = List.objects.get(pk=list_id)
	task.completed=False
	task.save()
	return redirect("home")

def edit(request,_id):
	print(_id)
	if request.method=='POST':
		task_to_be_edited = Task.objects.get(pk = _id)
		form = TaskForm(request.POST or None, instance=task_to_be_edited)

		if form.is_valid():
			form.save()
			messages.success(request,('task has been edited successfully...'))
			task_home_id = Task.objects.get(pk=_id)
			print(task_home_id.listid.id)
			task_home_id = task_home_id.listid.id
			return redirect('task_home',task_home_id)
	else:
		task = Task.objects.get(pk=_id)
		return render(request,'edit.html',{'task':task})
