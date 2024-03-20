from rest_framework import serializers

from posts.models import Post, Comments, likes
from profiles.serializers import CompactUserProfileSerializer
from profiles.models import UserProfile


class PostGetSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to handle Post related task.
    """
    user = CompactUserProfileSerializer()
    image = serializers.FileField()
    video = serializers.FileField()
    class Meta:
        model = Post
        fields = ["id", "user", "content", "created_at", "image", "video"]


class PostCreateSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to handle Post related task.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    image = serializers.FileField(required=False)
    video = serializers.FileField(required=False)
    class Meta:
        model = Post
        fields = ["id", "user", "content", "created_at", "image", "video"]

class CommentSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to handle Post Comments related task.
    """
    user = CompactUserProfileSerializer()
    class Meta:
        model = Comments
        fields = ["id", "comment", "user"]


class LikesSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to handle Post likes related task.
    """
    user = CompactUserProfileSerializer()
    class Meta:
        model = likes
        fields = ["id", "user"]