from django.contrib import admin

from friends.models import UserFollowing
# Register your models here.


@admin.register(UserFollowing)
class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'follower', 'status')
    list_filter = ('status', )
    fields = ['user', 'follower', 'status']