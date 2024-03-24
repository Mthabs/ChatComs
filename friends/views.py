from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404

from friends.models import UserFollowing
from friends.serializers import FollowerListSerializer, FollowingListSerializer
from profiles.models import UserProfile
from profiles.utils import search_user_profile
from profiles.serializers import CompactUserProfileSerializer


class ManageFollowerView(APIView):
    """
    APIView Instance to fetch followers list
    """
    serializer_class = FollowerListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Returns List of followers, of logged in User.
        user_profile = UserProfile.objects.get(user=request.user)
        try:
            follower_list = get_list_or_404(UserFollowing, user=user_profile)
            data = self.serializer_class(follower_list, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response([], status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        # Accepts Following request. 
        instance = self.fetch_follower(pk)
        instance.status = "accepted"
        instance.save()
        return Response({"message": "Following request accepted"}, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk):
        # Remove Follower, depreciated view.
        instance = self.fetch_follower(pk)
        instance.delete()
        return Response({"message":"Removed Follower"}, status=status.HTTP_204_NO_CONTENT)
      
    def fetch_follower(self, pk):
        return get_object_or_404(UserFollowing, id=pk)
    

class ManageFollowingView(APIView):
    """
    APIView Instance to fetch followers list
    """
    serializer_class = FollowingListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Returns List of following, of logged in User.
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            following_list = get_list_or_404(UserFollowing, follower=user_profile)
            data = self.serializer_class(following_list, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response([], status=status.HTTP_200_OK)
    
    def post(self, request, fk):
        #View to follow a user.
        friend_instance = self.fetch_userprofile(fk)
        user = self.fetch_current_user(request)
        try:
            instance = UserFollowing.objects.create(user=friend_instance, follower=user)
            return Response({"message": "Following Request is sent", "id":instance.id}, status=status.HTTP_201_CREATED)
        except Exception as exc:
            return Response({"message": f"Error Occurred {str(exc).strip("\n")}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        #Remove Following/ Unfollow user.
        instance = self.fetch_following(pk)
        instance.delete()
        return Response({"message":"Removed Follower"}, status=status.HTTP_204_NO_CONTENT)
    
    def fetch_following(self, pk):
        return get_object_or_404(UserFollowing, id=pk)
    
    def fetch_userprofile(self, fk):
        return get_object_or_404(UserProfile, id=fk)
    
    def fetch_current_user(self, request):
        return get_object_or_404(UserProfile, user=request.user)
    
class CheckFollowingView(APIView):
    """
    API INSTANCE TO CHECK IF USER IS FOLLOWING
    """
    def get(self, request, fk):
        current_user = self.fetch_current_user(request)
        user = self.get_user_by_id(fk)
        try:
            relation = UserFollowing.objects.get(user=user, follower=current_user)
            return Response({"id":relation.id, "status":relation.status}, status=status.HTTP_200_OK)
        except:
            return Response({"follow":False}, status=status.HTTP_200_OK)

    def fetch_current_user(self, request):
        return get_object_or_404(UserProfile, user=request.user)

    def get_user_by_id(self, fk):
        return get_object_or_404(UserProfile, id=fk)
    
class UserProfileSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('query', None)
        
        if not query:
            return Response("Query parameter 'query' is required", status=status.HTTP_400_BAD_REQUEST)

        user_profiles = search_user_profile(query)
        serializer = CompactUserProfileSerializer(user_profiles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)