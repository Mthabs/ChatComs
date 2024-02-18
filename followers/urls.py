from django.urls import path
from .views import FollowerListCreateView, FollowerUnfollowView

urlpatterns = [
    path('followers/', FollowerListCreateView.as_view(), name='follower-list-create'),
    path('followers/<int:pk>/', FollowerUnfollowView.as_view(), name='follower-unfollow'),
]