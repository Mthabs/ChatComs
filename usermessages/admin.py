from django.contrib import admin

from usermessages.models import UserChat, UserMessage

# Register your models here.
@admin.register(UserChat)
class UserChatAdmin(admin.ModelAdmin):
    list_display = ("id",  "user_a", "user_b", "last_update")
    fields = ("user_a", "user_b", "usera_last_seen", "userb_last_seen")

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "chat",  "sender", "created", "is_deleted", "is_viewed")
    fields = ("message", "image", "video", "chat", "receiver", "sender", "is_deleted", "is_viewed")
    list_filter = ("is_deleted", "is_viewed")
    
    
    
    
