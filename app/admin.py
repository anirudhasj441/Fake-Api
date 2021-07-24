from django.contrib import admin
from .models import Client, Project, UserExtend

# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'client_name',
        'created_at',
        'created_by'
    ]

class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'project_name',
        'client_name',
        'user_list',
        'created_at'
    ]
    def user_list(self, obj):
        users = ''
        for user in obj.users.all():
            users += user.username+","
        return users
    def client_name(self,obj):
        return obj.client.client_name

admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(UserExtend)