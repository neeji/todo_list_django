from django.urls import path
from . import views
urlpatterns = [
   path('',views.home,name='home'),
   path('task_home/<list_id>',views.task_home,name='task_home'),
   path('delete/<_id>',views.delete,name='delete'),
   path('cross_off/<_id>',views.cross_off,name='cross_off'),
   path('uncross/<_id>',views.uncross,name='uncross'),
   path('edit/<_id>',views.edit,name='edit'),
   path('delete_list/<list_id>',views.delete_list,name='delete_list'),
]