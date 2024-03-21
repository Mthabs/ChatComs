from rest_framework import serializers

from friends.models import UserFollowing
from profiles.serializers import CompactUserProfileSerializer


class FollowerListSerializer(serializers.ModelSerializer):
    """
    ModelSerializer Class to fetch list of User Followers
    """
    user = CompactUserProfileSerializer(source="follower")
    class Meta:
        model = UserFollowing
        fields = ['id', 'user']

class FollowingListSerializer(serializers.ModelSerializer):
    """
    ModelSerializer Class to fetch list of User Following.
    """
    user = CompactUserProfileSerializer()
    class Meta:
        model = UserFollowing
        fields = ['id', 'user']