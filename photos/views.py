from rest_framework import generics, permissions, filters
from friends_chats.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from .models import Photo
from .serializers import PhotoSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class PhotoListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = [MultiPartParser, FormParser]

    
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        'owner__username',
        'caption',
    ]
    ordering_fields = [
        'like_count',
        'comment_count',
        'likephotos__created_at',
    ]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, image=self.request.data.get('image'))

class PhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer