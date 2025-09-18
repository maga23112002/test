from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tasks import views as task_views
from tasks.forms import CustomLoginForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')), 
    path('', task_views.index, name='index'),  
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        authentication_form=CustomLoginForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', task_views.register, name='register'),
]
