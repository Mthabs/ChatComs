from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404

from posts.serializers import PostGetSerializer, PostCreateSerializer
from posts.models import Post
from profiles.models import UserProfile


class PostView(APIView):
    """
    APIView Instance to a
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostGetSerializer

    def get(self, request, pk=None):
        if pk:
            post = self.fetch_post_by_id(pk)
            serializer = self.serializer_class(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = self.fetch_user_profile(request)
            posts = self.fetch_user_posts(user)
            serializer = self.serializer_class(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            serializer = PostCreateSerializer(data=request.data, context = {"request":request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    "message": "Post Created",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
        except Exception as exc:
            return Response({
                "message": "Error occured",
                "error": str(exc).strip("\n")
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        instance = self.fetch_post_by_id(pk)
        instance.delete()
        return Response({
            "message": "Post is deleted"
        }, status=status.HTTP_204_NO_CONTENT)

    def fetch_post_by_id(self, pk):
        return get_object_or_404(Post, id=pk)

    
    def fetch_user_profile(self, request):
       return get_object_or_404(UserProfile, user=request.user)

    def fetch_user_posts(self, user):
        return get_list_or_404(Post, user=user)
    
class GetAllPosts(APIView):
    """
    API Instance View to fetch all Posts
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostGetSerializer
    def get(self, request):
        instances = Post.objects.all()
        count = instances.count()
        serializer = self.serializer_class(instances, many=True)
        return Response({
            'count':count,
            'posts':serializer.data
        }, status=status.HTTP_200_OK)

class UserPosts(APIView):
    """
    API Instance View to fetch all Specific Users Posts
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostGetSerializer
    def get(self, request, fk):
        userprofile = self.fetch_user_profile(fk)
        instances = Post.objects.filter(user=userprofile)
        count = instances.count()
        serializer = self.serializer_class(instances, many=True)
        return Response({
            'count':count,
            'posts':serializer.data
        }, status=status.HTTP_200_OK)
    
    def fetch_user_profile(self, fk):
        return get_object_or_404(UserProfile, id=fk)