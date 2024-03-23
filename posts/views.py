from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404

from posts.serializers import PostGetSerializer, PostCreateSerializer, CommentSerializer, CommentGetSerializer
from posts.models import Post, Likes, Comments, CommentLikes
from profiles.models import UserProfile



class PostView(APIView):
    """
    APIView Instance
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostGetSerializer

    def get(self, request, pk=None):
        if pk:
            # Fetch Post by ID.
            post = self.fetch_post_by_id(pk)
            serializer = self.serializer_class(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            #Fetch all users posts.
            user = self.fetch_user_profile(request)
            posts = self.fetch_user_posts(user)
            serializer = self.serializer_class(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        #Create New Post.
        try:
            serializer = PostCreateSerializer(data=request.data, context = {"request":request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({ "message": "Post Created", "data": serializer.data }, status=status.HTTP_201_CREATED)
        except Exception as exc:
            return Response({ "message": "Error occured", "error": str(exc).strip("\n") }, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        #Delete Post Instance.
        instance = self.fetch_post_by_id(pk)
        instance.delete()
        return Response({ "message": "Post is deleted" }, status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
        #Update Post Instance.
        instance = self.fetch_post_by_id(pk)
        try:
            serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "Post Updated Successfully"}, status=status.HTTP_206_PARTIAL_CONTENT)
        except Exception as exc:
            return Response({ "message": "Error occured", "error": str(exc).strip("\n")}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({ 'count':count, 'posts':serializer.data }, status=status.HTTP_200_OK)
    

class UserPosts(APIView):
    """
    API Instance View to fetch all Specific Users Posts, Not logged In user
    """
    permission_classes = [IsAuthenticated] #Update Query Set
    serializer_class = PostGetSerializer
    def get(self, request, fk):
        userprofile = self.fetch_user_profile(fk)
        instances = Post.objects.filter(user=userprofile)
        count = instances.count()
        serializer = self.serializer_class(instances, many=True)
        return Response({ 'count':count, 'posts':serializer.data }, status=status.HTTP_200_OK)
    
    def fetch_user_profile(self, fk):
        return get_object_or_404(UserProfile, id=fk)
    
    
class PostLikeView(APIView):
    """
    API Instance to manage post likes
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, fk):
        post = self.fetch_post(fk)
        userprofile = self.fetch_user_profile(request)
        try:
            if Likes.objects.filter(post=post, user=userprofile).exists():
                return Response({"like":True}, status=status.HTTP_200_OK)
        except Exception as exc:
            pass
        return Response({"like":False}, status=status.HTTP_200_OK)
        
    def post(self, request, fk):
        post = self.fetch_post(fk)
        userprofile = self.fetch_user_profile(request)
        try:
            Likes.objects.get_or_create(user=userprofile, post=post)
            return Response({"message":"Like successfully"}, status=status.HTTP_200_OK)
        except Exception as exc:
            return Response({"errors":str(exc).strip("\n")})
        
    def delete(self, request, fk):
        post = self.fetch_post(fk)
        userprofile = self.fetch_user_profile(request)
        try:
            instance = Likes.objects.get(user=userprofile, post=post)
            instance.delete()
        except:
            print("Like object doesn't exist")
        return Response({"message":"Successfully unliked"}, status=status.HTTP_204_NO_CONTENT)

    def fetch_post(self, fk):
        return get_object_or_404(Post, id=fk)
    
    def fetch_user_profile(self, request):
        return get_object_or_404(UserProfile, user=request.user)
    

class CommentsView(APIView):
    """
    APIView Instance to perform Read operation on Comment Model
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentGetSerializer

    def get(self, request, fk):
        post = self.get_post_by_id(fk)
        comments = Comments.objects.filter(post=post)
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_post_by_id(self, fk):
        return get_object_or_404(Post, id=fk)
    

class CommentsCreateView(APIView):
    """
    An APIView instance to create new Comments.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Message": "Comment created"}, status=status.HTTP_201_CREATED)
        
class ModifyCommentView(APIView):
    """
    An APIView instance to Modify and Delete Comments.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def patch(self, request, pk):
        instance = self.fetch_comment_by_id(pk)
        serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Message":"Comment has been updated"}, status=status.HTTP_206_PARTIAL_CONTENT)
        
    def delete(self, request, pk):
        instance = self.fetch_comment_by_id(pk)
        instance.delete()
        return Response({"Message":"Comment deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def fetch_comment_by_id(self, pk):
        return get_object_or_404(Comments, id = pk)
    

class HandleCommentLikeView(APIView):
    """
    APIView Instance to handle Comments likes
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, fk):
        user = self.fetch_current_user(request)
        comment = self.fetch_comment_by_id(fk)
        exists = CommentLikes.objects.filter(user=user, comment=comment).exists()
        return Response({"like":exists}, status=status.HTTP_200_OK)

    def post(self, request, fk):
        user = self.fetch_current_user(request)
        comment = self.fetch_comment_by_id(fk)
        CommentLikes.objects.get_or_create(user=user, comment=comment)
        return Response({"Message":"Liked comment"}, status=status.HTTP_200_OK)

    def delete(self, request, fk):
        user = self.fetch_current_user(request)
        comment = self.fetch_comment_by_id(fk)
        try:
            instance = CommentLikes.objects.filter(user=user, comment=comment)
            instance.delete()
        except:
            pass
        return Response({"Message":"Successfully unliked"}, status=status.HTTP_204_NO_CONTENT)
    
    def fetch_current_user(self, request):
        return get_object_or_404(UserProfile, user=request.user)
    
    def fetch_comment_by_id(self, fk):
        return get_object_or_404(Comments, id=fk)

    