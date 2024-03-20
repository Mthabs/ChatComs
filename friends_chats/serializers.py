from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from allauth.account.adapter import get_adapter
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CurrentUserSerializer(UserDetailsSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('profile_id', 'profile_image')


class CustomRegisterSerializer(RegisterSerializer):
    def custom_signup(self, request, user):
        # Skip email verification by setting email address as verified
        user.is_active = True
        user.save()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']



