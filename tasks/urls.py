from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.user_tasks, name='user_tasks'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),

    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/tasks/', views.manage_tasks, name='manage_tasks'),
    path('admin-panel/users/', views.manage_users, name='manage_users'),
    path('admin-panel/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin-panel/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
]
