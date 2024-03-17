from rest_framework import serializers

from friends.models import UserFollowing


class FollowerListSerializer(serializers.ModelSerializer):
    """
    ModelSerializer Class to fetch list of User Followers
    """
    name = serializers.ReadOnlyField(source='follower.name')
    profile_picture = serializers.ReadOnlyField(source='follower.profile_picture')
    class Meta:
        model = UserFollowing
        fields = ['id', 'follower', 'profile_picture', 'name', 'status']

class FollowingListSerializer(serializers.ModelSerializer):
    """
    ModelSerializer Class to fetch list of User Following.
    """
    name = serializers.ReadOnlyField(source='user.name')
    profile_picture = serializers.ReadOnlyField(source='user.profile_picture')
    class Meta:
        model = UserFollowing
        fields = ['id', 'user', 'profile_picture', 'name', 'status']