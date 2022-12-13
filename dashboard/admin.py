from django.contrib import admin
from django.contrib.auth.models import User
from django_celery_results.admin import GroupResult, TaskResultAdmin
from django_celery_results.models import TaskResult

from .models import UserTask


class CustomTaskResultAdmin(TaskResultAdmin):
    list_display = (
        'task_id', 
        'task_name', 
        'status', 
        'task_kwargs', 
        'result', 
        'date_created', 
        'date_done'
    )

class UserTaskAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'email', 
        'first_name', 
        'last_name', 
        'task', 
        'task_name', 
        'date_created', 
        'date_completed'
    )
    readonly_fields = ('user', 'task')
    
    def get_user_object(self, obj):
        user_object = User.objects.get(id=obj.user.id)
        return user_object
    
    def email(self, obj):
        return self.get_user_object(obj).email
    
    def first_name(self, obj):
        return self.get_user_object(obj).first_name
    
    def last_name(self, obj):
        return self.get_user_object(obj).last_name
    
    def get_task_object(self, obj):
        task_object = TaskResult.objects.get(task_id=obj.task.task_id)
        return task_object
    
    def task_id(self, obj):
        return self.get_task_object(obj).task_id
    
    def task_name(self, obj):
        return self.get_task_object(obj).task_name
    
    def task_status(self, obj):
        return self.get_task_object(obj).status
    
    def date_created(self, obj):
        return self.get_task_object(obj).date_created
    
    def date_completed(self, obj):
        return self.get_task_object(obj).date_done
    
admin.site.unregister(GroupResult)
admin.site.unregister(TaskResult)

admin.site.register(TaskResult, CustomTaskResultAdmin)
admin.site.register(UserTask, UserTaskAdmin)
