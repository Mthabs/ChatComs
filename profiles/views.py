from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from profiles.models import UserProfile
from profiles.serializers import UserProfileSerializer, CreateUserProfileSerializer


class UserProfileView(APIView):
    """
    Instance of APIView to Manage User Profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        userprofile = self.fetch_userprofile(request)
        serializer = UserProfileSerializer(userprofile, context={'request': request})
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        try:
            user_profile = self.fetch_userprofile(request)
            serializer = CreateUserProfileSerializer(instance=user_profile, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    "message": "Profile Updated",
                    "data" : serializer.data
                }, status=status.HTTP_206_PARTIAL_CONTENT)
        except Exception as exc:
            return Response({
                "message": "Error(s) occurred while trying to update profile",
                "exception": str(exc).strip("\n")
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def fetch_userprofile(self, request):
        return get_object_or_404(UserProfile, user=request.user)
    
class CreateUserProfile(APIView):
    """
    Instance of APIView to Create User Profile
    """
    serializer_class = CreateUserProfileSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response( serializer.data, status=status.HTTP_201_CREATED )
        except Exception as exc:
            return Response ({"message": f"Error occured {str(exc).strip("\n")}"}, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileDetailView(APIView):
    """
    Instance of APIView to Create User Profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        userprofile = self.fetch_user_by_id(pk)
        serializer = self.serializer_class(userprofile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def fetch_user_by_id(self, pk):
        return get_object_or_404(UserProfile, id=pk)

class ProfileEditView(APIView):
    """
    APIView instance to edit profile
    """
    serializer_class = CreateUserProfileSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        profile = self.fetch_profile_by_id(pk)
        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        profile = self.fetch_profile_by_id(pk)
        serializer = self.serializer_class(instance=profile, data=request.data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
        except Exception as exc:
            return Response({"error":str(exc).strip("\n")})

    def fetch_profile_by_id(self, pk):
        return get_object_or_404(UserProfile, id=pk)
