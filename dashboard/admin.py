from django.contrib import admin

from .models import UserTask


class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'task')
    readonly_fields = ('user', 'task')

admin.site.register(UserTask, UserTaskAdmin)
