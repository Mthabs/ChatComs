from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='image/', null=True, blank=True)
    status = models.TextField(blank=True, null=True)
    cover_photo = models.ImageField(upload_to='image/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_seen = models.DateTimeField(_("Last Seen"), auto_now=False, auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def fetch_username(self):
        return self.user.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
