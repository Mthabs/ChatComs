from rest_framework import serializers
from django.db import IntegrityError, transaction
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['id', 'post', 'owner', 'created_at']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"error" : "You have already liked this post."})