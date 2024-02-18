from django.urls import path
from .views import LikeListCreateView, LikeUnlikeView  

urlpatterns = [
    path('likes/', LikeListCreateView.as_view(), name='like-list-create'),
    path('likes/<int:pk>/', LikeUnlikeView.as_view(), name='like-Unlike'),
]