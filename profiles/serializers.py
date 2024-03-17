from rest_framework import serializers
from django.shortcuts import get_object_or_404
from profiles.models import UserProfile
from friends.models import UserFollowing


class CreateUserProfileSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to Create Userprofile details
    """
    class Meta:
        model = UserProfile
        fields = "__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to Fetch Userprofile details
    """
    username = serializers.SerializerMethodField()
    profile_picture = serializers.FileField()
    cover_photo = serializers.FileField()
    # posts_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'profile_picture', 'cover_photo', 'followers_count', 'following_count' ]

    # def get_profile_picture(self, obj):
    #     if obj.profile_picture:
    #         return obj.profile_picture
    #     else:
    #         #Freepik free to use picture
    #         return 'https://img.freepik.com/free-vector/illustration-businessman_53876-5856.jpg?w=740&t=st=1710659219~exp=1710659819~hmac=996a852ae757087525e6f08777ed883706c97f6f0ac40fcf9cf72d63d320cd67'
    
    # def get_cover_photo(self, obj):
    #     if obj.cover_photo:
    #         return obj.cover_photo
    #     else:
    #         return 'https://images.unsplash.com/photo-1505533321630-975218a5f66f?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'

    def get_followers_count(self, obj):
        user = self.fetch_userprofile()
        return UserFollowing.objects.filter(user=user).count()

    def get_following_count(self, obj):
        user = self.fetch_userprofile()
        return UserFollowing.objects.filter(follower=user).count()
    
    def get_username(self, obj):
        return obj.fetch_username
    # def get_posts_count(self, obj):
    #     return obj.owner.posts.all().count()

    def fetch_userprofile(self):
        request = self.context.get('request')
        return get_object_or_404(UserProfile, user=request.user)