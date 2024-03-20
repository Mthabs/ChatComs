from django.urls import path
from friends.views import ManageFollowerView, ManageFollowingView, CheckFollowingView

urlpatterns = [
    path('follower/', ManageFollowerView.as_view(), name='fetch-followers-list'),
    path('follower/<int:pk>/', ManageFollowerView.as_view(), name='manage-follower'),
    path('following/', ManageFollowingView.as_view(), name='fetch-following-list'),
    path('following/remove/<int:pk>/', ManageFollowingView.as_view(), name='remove-following'),
    path('following/add/<int:fk>/', ManageFollowingView.as_view(), name="add-following"),
    path('check/<int:fk>/', CheckFollowingView.as_view(), name='check-following'),
]