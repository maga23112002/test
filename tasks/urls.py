from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.user_tasks, name='user_tasks'),  # Главная страница задач пользователя
    path('tasks/add/', views.add_task, name='add_task'),  # Страница добавления новой задачи
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),  # Страница редактирования задачи
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),  # Страница удаления задачи
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),  # Админская панель
    path('admin-panel/tasks/', views.manage_tasks, name='manage_tasks'),  # Управление задачами
    path('admin-panel/users/', views.manage_users, name='manage_users'),  # Управление пользователями

]
