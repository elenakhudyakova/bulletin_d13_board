from django.contrib import admin
from .models import *

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'creation', 'category', 'title', 'content']
    list_filter = ['author', 'category']
    search_fields = ['author__username', 'title', 'content']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'creation', 'text_wrap', 'approved']
    search_fields = ['text', 'creation', 'user__username']
    list_filter = ['user', 'approved']

    def text_wrap(self, obj):
        return obj.text[:50]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
