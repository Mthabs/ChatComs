from django.db.models import Count
from django.db import models
from django.contrib.auth.models import User
from followers.models import Follower
#from friends.models import Friend

class UserProfile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='image/', null=True, blank=True)
    cover_photo = models.ImageField(upload_to='image/', null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"

    def get_posts_count(self):
        return self.posts.all().count()
