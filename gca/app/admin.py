from django.contrib import admin
from . models import Group, Chat
# Register your models here.


class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(Group, GroupModelAdmin)

class ChatModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'timestamp', 'group']

admin.site.register(Chat, ChatModelAdmin)
