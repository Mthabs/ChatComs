from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models import UserProfile


FOLLOWER_STATUS = [
    ("requested", "Following Requested"),
    ("accepted", "Follower"),
]
class UserFollowing(models.Model):
    user = models.ForeignKey(UserProfile, related_name='User', on_delete=models.CASCADE)
    follower = models.ForeignKey(UserProfile, related_name='follower', on_delete=models.CASCADE)
    status = models.CharField(_("Following status"), max_length=50, choices=FOLLOWER_STATUS, default="requested")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'follower']

    def __str__(self):
        return f'{self.follower} is following {self.user}'
