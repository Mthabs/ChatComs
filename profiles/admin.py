from django.contrib import admin
from profiles.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'first_name', 'last_name', 'profile_picture', 'status', 'cover_photo']
    list_display = ('id', 'user', 'first_name', 'last_name', 'created_at', 'updated_at')