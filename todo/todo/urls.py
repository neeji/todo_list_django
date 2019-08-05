from django.contrib import admin
from django.urls import path, include
from todo_list import views
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('todo_list.urls')),
    path('register/',user_views.register,name='register'),
    path('email/<list_id>/<user_name>',user_views.email,name='email'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'), 
]
