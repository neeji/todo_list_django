from tastypie.resources import ModelResource
from todo_list.models import List,Task,Share
from django.contrib.auth.models import User


class ListResource(ModelResource):
    class Meta:
        queryset = Share.objects.all()
        # allowed_methods = ['get']