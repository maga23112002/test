from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

# Регистрация
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Главная страница задач пользователя
@login_required
def index(request):
    return render(request, 'index.html')

# Просмотр всех задач пользователя
@login_required
def user_tasks(request):
    tasks = Task.objects.filter(owner=request.user)  # Фильтруем задачи по пользователю
    return render(request, 'tasks/user_tasks.html', {'tasks': tasks})

# Добавление новой задачи
@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user  # Привязываем задачу к текущему пользователю
            task.save()
            return redirect('user_tasks')  # Перенаправляем на страницу задач
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})

# Редактирование задачи
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)  
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('user_tasks')  
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})

# Удаление задачи
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)  
    task.delete()
    return redirect('user_tasks') 



def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:  
            return HttpResponseForbidden("Доступ запрещен. Только для администраторов.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Страница админской панели
@login_required
@admin_required
def admin_panel(request):
    return render(request, 'admin_panel.html')

# Страница управления задачами
@login_required
@admin_required
def manage_tasks(request):
    tasks = Task.objects.all()  
    return render(request, 'manage_tasks.html', {'tasks': tasks})

# Страница управления пользователями
@login_required
@admin_required
def manage_users(request):
    users = User.objects.all()  
    return render(request, 'manage_users.html', {'users': users})
