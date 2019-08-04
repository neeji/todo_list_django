from django.shortcuts import render,redirect
from .models import List
from .forms import ListForm
from django.contrib import messages


def home(request):
	# return render(request,"home.html",{})
	if request.method == 'POST':
		form = ListForm(request.POST or None)

		if form.is_valid():
			form.save()
			# all_tasks = List.objects.all()
			messages.success(request,("task has been added to the List Successfully..."))
			return redirect("home")
			# return render(request,'home.html',{'all_tasks':all_tasks})
	else:
		all_tasks = List.objects.all()
		return render(request,'home.html',{'all_tasks':all_tasks})


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

def edit(request,list_id):
	if request.method=='POST':
		task = List.objects.get(pk = list_id)
		form = ListForm(request.POST or None, instance=task)

		if form.is_valid():
			form.save()
			messages.success(request,('task has been edited successfully...'))
			return redirect('home')
	else:
		task = List.objects.get(pk=list_id)
		return render(request,'edit.html',{'task':task})
