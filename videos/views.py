from rest_framework import generics, permissions, filters
from friends_chats.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class VideoListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    parser_classes = [MultiPartParser, FormParser]


    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'like_count',
        'comment_count',
        'likevideos__created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, video_file=self.request.data.get('video_file'))

class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer