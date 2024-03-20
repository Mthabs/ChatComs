from django.db import models
from django.utils.translation import gettext_lazy as _
from cloudinary_storage.storage import VideoMediaCloudinaryStorage

from profiles.models import UserProfile


class Post(models.Model):
    """
    Users POST
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video = models.ImageField(upload_to='post_images/', storage=VideoMediaCloudinaryStorage(), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.user}"
    
    
class Comments(models.Model):
    """
    Post Comment
    """
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    comment = models.TextField(_("Users Comment"))
    user = models.ForeignKey(UserProfile, verbose_name=_("Commented User"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class likes(models.Model):
    """
    Post Like
    """
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name=_("Commented User"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)