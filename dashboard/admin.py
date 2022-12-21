from django.contrib import admin
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars
from django_celery_results.admin import GroupResult, TaskResultAdmin
from django_celery_results.models import TaskResult

from .models import Dataset, Function, Optimizer, TransferFunction, UserTask


class CustomTaskResultAdmin(TaskResultAdmin):
    list_display = (
        'task_id',
        'status',
        'task_name', 
        'task_kwargs', 
        'short_result', 
        'date_created',
        'date_done'
    )
    list_filter = ('task_name', 'status', 'date_created', 'date_done')
    ordering = ('-date_created', )
    
    # Shorten result
    def short_result(self, obj):
        return truncatechars(obj.result, 80)

    # Remove permissions
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

class UserTaskAdmin(admin.ModelAdmin):
    date_hierarchy = 'task__date_done'
    list_display = (
        'username', 
        'email',
        'task_id',
        'task_state', 
        'task_name', 
        'created_datetime', 
        'completed_datetime'
    )
    list_filter = (
        'user__username', 
        'task__task_name',
        'task__status', 
        'task__date_created', 
        'task__date_done'
    )
    readonly_fields = ('user', 'task')
    search_fields = (
        'user__username',
        'user__email',
        'task__task_id',
        'task__status',
        'task__task_name'
    )
    
    # Retrieve more user fields
    def get_user_object(self, obj):
        user_object = User.objects.get(id=obj.user.id)
        return user_object
    
    def username(self, obj):
        return self.get_user_object(obj).username
    
    def email(self, obj):
        return self.get_user_object(obj).email
    
    # Retrieve more task fields
    def get_task_object(self, obj):
        task_object = TaskResult.objects.get(task_id=obj.task.task_id)
        return task_object
    
    def task_id(self, obj):
        return self.get_task_object(obj).task_id
    
    def task_name(self, obj):
        return self.get_task_object(obj).task_name
    
    def task_state(self, obj):
        return self.get_task_object(obj).status
    
    def created_datetime(self, obj):
        return self.get_task_object(obj).date_created
    
    def completed_datetime(self, obj):
        return self.get_task_object(obj).date_done
    
    # Remove permissions
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

class FunctionAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'optimal_result')

admin.site.unregister(GroupResult)
admin.site.unregister(TaskResult)

admin.site.register(TaskResult, CustomTaskResultAdmin)
admin.site.register(UserTask, UserTaskAdmin)

admin.site.register(Optimizer)
admin.site.register(Function, FunctionAdmin)
admin.site.register(Dataset)
admin.site.register(TransferFunction)