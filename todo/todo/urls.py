from django.contrib import admin
from django.urls import path, include
from todo_list import views
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf.urls import url
from tastypie.api import Api
from .api import ListResource, TaskResource, SharedWithMeResource, UserResource, SharedByMeResource

# list_resource = ListResource()
# task_resource = TaskResource()
# shared_resource = SharedResource()
# user_resource = UserResource()
v1_api = Api(api_name='v1')
v1_api.register(ListResource())
v1_api.register(TaskResource())
v1_api.register(SharedWithMeResource())
v1_api.register(SharedByMeResource())
v1_api.register(UserResource())
# v1_api.register(LoginResource())

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('todo_list.urls')),
    path('register/',user_views.register,name='register'),
    path('email/<list_id>/<user_name>',user_views.email,name='email'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    # url(r'^api/',include(list_resource.urls)),
    # url(r'^api/',include(task_resource.urls)),
    # url(r'^api/',include(shared_resource.urls)),
    path('api/',include(v1_api.urls)),
    # path('api/',include(task_resource.urls)),
    # path('api/',include(shared_resource.urls)),
    # path('api/',include(user_resource.urls)),
]
