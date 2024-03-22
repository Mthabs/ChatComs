from django.contrib import admin
from posts.models import  Post, Comments, Likes


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['user', 'content']
    list_display = ['id', 'user', 'content']
    fields = ['user', 'content', 'image', 'video']
    list_filter = ['user',]



@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    fields = ['post', 'user', 'comment', 'created_at']
    list_display = ['id', 'post', 'user', 'comment', 'created_at']


@admin.register(Likes)
class likesAdmin(admin.ModelAdmin):
    fields = ['post', 'user',  'created_at']
    list_display = ['id', 'post', 'user', 'created_at']