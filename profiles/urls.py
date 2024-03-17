from django.urls import path
from .views import UserProfileView, CreateUserProfile


urlpatterns = [
    path('', UserProfileView.as_view(), name='profile-detail'),
    path('create/', CreateUserProfile.as_view(), name='profile-list-create'),
]