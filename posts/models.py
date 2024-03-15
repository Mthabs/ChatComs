from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    header = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post_picture = models.ImageField(upload_to='post_images/', null=True, blank=True)
    content = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.id} at {self.header}"

        blank=True,

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()
