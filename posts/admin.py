from django.contrib import admin
from posts.models import PostMedia, Post, Comments, likes


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['user', 'content', 'media']
    list_display = ['id', 'user', 'content', 'media']
    list_filter = ['user',]


@admin.regiser(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    readonly_fields = ['image', 'video']


@admin.regiser(Comments)
class CommentsAdmin(admin.ModelAdmin):
    fields = ['post', 'user', 'comment', 'created_at']
    list_display = ['id', 'post', 'user', 'comment', 'created_at']


@admin.regiser(likes)
class likesAdmin(admin.ModelAdmin):
    fields = ['post', 'user',  'created_at']
    list_display = ['id', 'post', 'user', 'created_at']