from rest_framework import serializers

from posts.models import Post, Comments,  Likes, CommentLikes
from profiles.serializers import CompactUserProfileSerializer
from profiles.models import UserProfile


class PostGetSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to handle Post related task.
    """
    user = CompactUserProfileSerializer()
    image = serializers.FileField()
    video = serializers.FileField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "user", "content", "created_at", "image", "video", "likes_count", "comments_count"]

    def get_likes_count(self, obj):
        return Likes.objects.filter(post=obj).count()

    def get_comments_count(self, obj):
        return Comments.objects.filter(post=obj).count()


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
        model = Likes
        fields = ["id", "user"]

class CommentSerializer(serializers.ModelSerializer):
    """
    ModelSerializer Instance to handle Create and Update operations
    """
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())

    class Meta:
        model = Comments
        fields = "__all__"

class CommentGetSerializer(serializers.ModelSerializer):
    """
    ModelSerializer instance to handle GET operations
    """
    user = CompactUserProfileSerializer()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ["id", "comment", "user", "created_at", "likes_count"]

    def get_likes_count(self, obj):
        return CommentLikes.objects.filter(comment=obj).count()