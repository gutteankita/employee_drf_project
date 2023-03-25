from django.contrib import admin
from Emp_App.models import *



# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_active', 'is_admin', 'is_user', 'created_at', 'updated_at']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age', 'gender', 'department', 'salary']

@admin.register(BlackListedToken)
class BlackListedTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'token', 'user', 'timestamp']
