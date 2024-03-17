from rest_framework import serializers

from posts.models import Post, PostMedia, Comments, likes
from profiles.serializers import CompactUserProfileSerializer


class PostMediaSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to handle Image Post related task.
    """
    image = serializers.FileField()
    video = serializers.FileField()
    class Meta:
        model = PostMedia
        fields = ["id", "image", "post", "video"]


class PostSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to handle Post related task.
    """
    user = CompactUserProfileSerializer()
    media = PostMediaSerializer()
    class Meta:
        model = Post
        fields = ["id", "user", "content", "created_at", "media"]


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