from django.shortcuts import render , redirect
from django.http import HttpResponse
from todolist.models import TaskList
from todolist.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
 

@login_required
def todolist(request):

    
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).manager = request.user
            form.save()
        messages.success(request, ('new task added'))    

        return redirect('todolist')    


    else:
        all_tasks = TaskList.objects.filter(manager=request.user)
        paginator  = Paginator(all_tasks, 5)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)
        return render(request , 'todolist.html' , {'all_tasks' : all_tasks})


@login_required
def contact(request):

    context = {'welcome_text' : "welcome to todo list app"}
    return render(request , 'contact.html' , context)
@login_required
def about(request):

    context = {'welcome_text' : "welcome to todo list app"}
    return render(request , 'about.html' , context)   

def index(request):

    context = {'welcome_text' : "welcome to todo list app"}
    return render(request , 'index.html' , context)   

def delete_task(request , task_id):

    task = TaskList.objects.get(pk=task_id)
    if task.manager == request.user:
        task.delete()
    else:
        messages.error(request, ('Access Restricted , you are not allowed '))

    return redirect('todolist')   


def edit_task(request , task_id):

    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None , instance= task)
        if form.is_valid():
            form.save()
         
        messages.success(request, ('Task edited '))    

        return redirect('todolist')    


    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request , 'edit.html' , {'task_obj' : task_obj })


def complete_task(request , task_id):

    task = TaskList.objects.get(pk=task_id)
    if task.manager == request.user:
        task.done = True
        task.save()
    else:
         messages.error(request, ('Access Restricted , you are not allowed '))      
    return redirect('todolist')   


def pending_task(request , task_id):

    task = TaskList.objects.get(pk=task_id)
    task.done = False
    task.save()
    return redirect('todolist')       