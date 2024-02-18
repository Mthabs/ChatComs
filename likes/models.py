from django.db import models
from django.contrib.auth.models import User

class Like(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='likes')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['post', 'owner']  

    def __str__(self):
        return f"Like by {self.owner} on Post {self.post}"


