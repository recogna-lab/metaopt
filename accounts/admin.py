from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User


class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_staff'
    )
    readonly_fields = ('id',)

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(User, CustomUserAdmin)
