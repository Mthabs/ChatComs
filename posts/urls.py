from django.urls import path
from posts.views import PostView, GetAllPosts, UserPosts, PostLikeView, CommentsCreateView, CommentsView, ModifyCommentView, HandleCommentLikeView

urlpatterns = [
    # Post-Related URLs
    path('', PostView.as_view(), name='post-list'),
    path('<int:pk>/', PostView.as_view(), name='post-detail'),
    path('all/', GetAllPosts.as_view(), name="fetch-all-view"),
    path('user/<int:fk>/', UserPosts.as_view(), name="user-specific-posts"),
    #Post-Like related URLs
    path('like/<int:fk>/', PostLikeView.as_view(), name="post-like"),
    #Post-Comment related URLs
    path("comment/create/", CommentsCreateView.as_view(), name="create-comment"),
    path("comment/fetch/<int:fk>/", CommentsView.as_view(), name="Comments-list"),
    path("comment/modify/<int:pk>/", ModifyCommentView.as_view(), name="update-delelte-comment"),
    #Comments Like Related URLs
    path("comment/like/<int:fk>/", HandleCommentLikeView.as_view(), name="Handle=comment-likes"),
]