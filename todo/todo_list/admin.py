from django.contrib import admin
from .models import Task,Share,List
# Register your models here.
admin.site.register(List)
admin.site.register(Task)
admin.site.register(Share)
