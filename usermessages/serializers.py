from rest_framework import serializers
from usermessages.models import UserChat, UserMessage
from profiles.serializers import CompactUserProfileSerializer
from profiles.models import UserProfile



class UserChatCreateSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to Create new Chat
    """
    user_a = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    user_b = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    class Meta:
        model = UserChat
        fields = ["user_a", "user_b"]


class UserChatGetSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to get list of UserChats
    """
    last_message = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    last_seen = serializers.SerializerMethodField()


    class Meta:
        model = UserChat
        fields = ["id", "user", "last_seen", "last_update", "last_message"]

    def get_user(self, obj):
        current_user = self.fetch_current_user()
        other_user = obj.user_a
        if current_user == other_user:
            other_user=obj.user_b
        serializer = CompactUserProfileSerializer(other_user)
        return serializer.data

    def get_last_message(self, obj):
        current_user = self.fetch_current_user()
        message_instance = UserMessage.objects.filter(chat=obj).order_by('-created').first()
        if message_instance:
            message = "Deleted Message" if message_instance.is_deleted  else message_instance.message
            data = {}
            if current_user == message_instance.sender:
                data['seen'] = True
                data['text'] = f"You : {message}"
            else:
                data['seen'] = message_instance.is_viewed
                data['text'] = f"{message_instance.sender.first_name} : {message}"
            data['sent'] = message_instance.created
            return data
        else:
            return None
    
    def get_last_seen(self, obj):
        current_user = self.fetch_current_user()
        if current_user != obj.user_a :
            return obj.usera_last_seen
        else:
            return obj.userb_last_seen
            
    def fetch_current_user(self):
        user = self.context['request'].user
        return UserProfile.objects.get(user=user)
    

class UserMessageCreateSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to create user message
    """
    chat = serializers.PrimaryKeyRelatedField(queryset=UserChat.objects.all())
    image = serializers.FileField(required=False)
    video = serializers.FileField(required=False)
    receiver = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    sender = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    class Meta:
        model = UserMessage
        fields = ['message', 'image', 'video', 'chat', 'receiver', 'sender']


class UserMessageFetchSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to fetch User Message detail
    """
    self = serializers.SerializerMethodField()
    sender = CompactUserProfileSerializer()
    message = serializers.SerializerMethodField()
    created = serializers.DateTimeField()
    class Meta:
        model = UserMessage
        fields = ['id', 'message', 'image', 'video', 'sender', 'created', 'is_deleted', 'self']

    def get_self(self, obj):
        currentuser = self. fetch_current_user()
        return currentuser == obj.sender
    
    def fetch_current_user(self):
        user = self.context['request'].user
        return UserProfile.objects.get(user=user)
    
    def get_message(self, obj):
        if obj.is_deleted:
            return "This message has been deleted"
        else:
            return obj.message
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created'] = instance.created.isoformat()
        return data


