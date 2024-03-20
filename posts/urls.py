from django.urls import path
from .views import PostView, GetAllPosts, UserPosts

urlpatterns = [
    path('', PostView.as_view(), name='post-list'),
    path('<int:pk>/', PostView.as_view(), name='post-detail'),
    path('all/', GetAllPosts.as_view(), name="fetch-all-view"),
    path('user/<int:fk>/', UserPosts.as_view(), name="user-specific-posts")
]