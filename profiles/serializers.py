from rest_framework import serializers
from django.shortcuts import get_object_or_404
from profiles.models import UserProfile
from friends.models import UserFollowing
from posts.models import Post


class CreateUserProfileSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to Create Userprofile details
    """
    profile_picture = serializers.FileField(required=False)
    class Meta:
        model = UserProfile
        fields = "__all__"
        

class UserProfileSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to Fetch Userprofile details
    """
    profile_picture = serializers.FileField()
    posts_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'profile_picture', 'followers_count', 'following_count', 'posts_count', 'full_name', 'status' ]

    def get_followers_count(self, obj):
        return UserFollowing.objects.filter(user=obj, status="accepted").count()

    def get_following_count(self, obj):
        return UserFollowing.objects.filter(follower=obj, status="accepted").count()
    
    def get_posts_count(self, obj):
        return Post.objects.filter(user=obj).count()
 
    def get_full_name(self, obj):
        return obj.full_name
    

class CompactUserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer to load userdetails for comments and likes
    """
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['id', 'full_name', 'profile_picture', 'last_seen']

    def get_full_name(self, obj):
        return obj.full_name
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['last_seen'] = instance.last_seen.isoformat()
        return data