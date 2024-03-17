from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404

from friends.models import UserFollowing
from friends.serializers import FollowerListSerializer, FollowingListSerializer
from profiles.models import UserProfile


class ManageFollowerView(APIView):
    """
    APIView Instance to fetch followers list
    """
    serializer_class = FollowerListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        follower_list = self.fetch_users_follower(request)
        data = self.serializer_class(follower_list, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        instance = self.fetch_follower(pk)
        instance.status = "accepted"
        instance.save()
    
    def destroy(self, request, pk):
        instance = self.fetch_follower(pk)
        instance.delete()
        return Response({"message":"Removed Follower"}, status=status.HTTP_204_NO_CONTENT)
    
    def fetch_users_follower(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        return get_list_or_404(UserFollowing, user=user_profile)
      
    def fetch_follower(self, pk):
        return get_object_or_404(UserFollowing, id=pk)
    

class ManageFollowingView(APIView):
    """
    APIView Instance to fetch followers list
    """
    serializer_class = FollowingListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_list = self.fetch_users_following(request)
        data = self.serializer_class(following_list, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request, fk):
        friend_instance = self.fetch_userprofile(fk)
        try:
            instance = UserFollowing.objects.create(user=friend_instance, follower=request.user)
            return Response({"message": "Following Request is sent"})
        except Exception as exc:
            return Response({"message": f"Error Occurred {str(exc).strip("\n")}"})
    
    def destroy(self, request, pk):
        instance = self.fetch_following(pk)
        instance.delete()
        return Response({"message":"Removed Follower"}, status=status.HTTP_204_NO_CONTENT)
    
    def fetch_users_following(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        return get_list_or_404(UserFollowing, follower=user_profile)
    
    def fetch_following(self, pk):
        return get_object_or_404(UserFollowing, id=pk)
    
    def fetch_userprofile(self, fk):
        return get_object_or_404(UserProfile, id=fk)
    


        

    
