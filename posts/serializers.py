from .models import Post
from PIL import Image
from rest_framework import serializers
from likes.models import Like
from comments.models import Comment

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_picture = serializers.ReadOnlyField(source='user.userprofile.profile_picture_url')
    is_owner = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'profile_id', 'owner', 'header', 'content','like_id', 'created_at', 'updated_at','profile_picture', 'post_picture', 'is_owner', 'image_filter','like_count', 'comment_count']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        default_post_picture_url = 'https://res.cloudinary.com/dnt7oro5y/image/upload/v1702078965/default_post_wv7bvz.jpg'
        default_profile_picture_url = 'https://res.cloudinary.com/dnt7oro5y/image/upload/v1702078965/default_profile_yansvo.jpg'

        if not instance.post_picture:
            representation['post_picture'] = default_post_picture_url

        if 'profile_picture' not in representation:
            representation['profile_picture'] = default_profile_picture_url

        return representation    

    def validate_post_picture(self, value):
        if value:
            max_size = 2 * 1024 * 1024  # 2 MB
            if value.size > max_size:
                raise serializers.ValidationError('Image size cannot exceed 2 MB.')

            try:
                with Image.open(value) as img:
                    width, height = img.size
                    if height > 4096:
                        raise serializers.ValidationError('Image height cannot exceed 4096px.')
                    if width > 4096:
                        raise serializers.ValidationError('Image width cannot exceed 4096px.')
            except (IOError, OSError) as e:
                raise serializers.ValidationError('Invalid image file.') from e

        return value

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        try:
            like = Like.objects.get(owner=user, post=obj)
            return like.id
        except Like.DoesNotExist:
            return None

    def get_like_count(self, obj):
        return obj.like_count

    def get_comment_count(self, obj):
        return obj.comment_count