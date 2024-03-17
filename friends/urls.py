from django.urls import path
from friends.views import ManageFollowerView, ManageFollowingView

urlpatterns = [
    # path('friends/', FriendListCreateView.as_view(), name='friend-list-create'),
    # path('friends/<int:pk>/', FriendUnfriendView.as_view(), name='friend-Unfriend'),
    path('follower/', ManageFollowerView.as_view(), name='fetch_followers list'),
    path('follower/<int:pk>/', ManageFollowerView.as_view(), name='manage_follower'),
    path('following/', ManageFollowingView.as_view(), name='fetch_following_list'),
    path('following/remove/<int:pk>/', ManageFollowingView.as_view(), name='remove_following')
    path('following/add/<int:pk>/')
]