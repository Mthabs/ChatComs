from django.urls import path
from .views import UserProfileView, CreateUserProfile, ProfileDetailView, ProfileEditView


urlpatterns = [
    path('', UserProfileView.as_view(), name='profile-detail'),
    path('create/', CreateUserProfile.as_view(), name='profile-list-create'),
    path('details/<int:pk>/', ProfileDetailView.as_view(), name='profile-details'),
    path('edit/<int:pk>/', ProfileEditView.as_view(), name='profileEdit-view')
]