from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def index(request):
    return render(request, 'index.html')

@login_required
def user_tasks(request):
    tasks = Task.objects.filter(owner=request.user)
    return render(request, 'tasks/user_tasks.html', {'tasks': tasks})

@login_required
def add_task(request):
    user_id = request.GET.get('user_id')  
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if user_id and request.user.is_staff:
                task.owner = get_object_or_404(User, id=user_id)
            else:
                task.owner = request.user
            task.save()
            return redirect(request.GET.get('next', 'user_tasks'))
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if not request.user.is_staff and task.owner != request.user:
        return HttpResponseForbidden("Вы не можете редактировать эту задачу.")
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            if request.user.is_staff:
                return redirect('manage_tasks')
            return redirect('user_tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if not request.user.is_staff and task.owner != request.user:
        return HttpResponseForbidden("Вы не можете удалить эту задачу.")
    task.delete()
    if request.user.is_staff:
        return redirect('manage_tasks')
    return redirect('user_tasks')


def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("Доступ запрещен. Только для администраторов.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@admin_required
def admin_panel(request):
    return render(request, 'admin_panel.html')

@login_required
@admin_required
def manage_tasks(request):
    tasks = Task.objects.all()
    return render(request, 'manage_tasks.html', {'tasks': tasks})

@login_required
@admin_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

@login_required
@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
    return redirect('manage_users')

@login_required
@admin_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        is_active = request.POST.get('is_active') == 'True'
        if username:
            user.username = username
            user.is_active = is_active
            user.save()
    return redirect('manage_users')
