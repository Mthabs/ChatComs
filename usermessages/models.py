from django.db import models
from django.utils.translation import gettext_lazy as _
from cloudinary_storage.storage import VideoMediaCloudinaryStorage

from profiles.models import UserProfile

# Create your models here.
class UserChat(models.Model):
    user_a = models.ForeignKey(UserProfile, verbose_name=_("User A"), on_delete=models.CASCADE, related_name="requesting_person")
    user_b = models.ForeignKey(UserProfile, verbose_name=_("User A"), on_delete=models.CASCADE, related_name="reciver_person")
    usera_last_seen = models.DateTimeField(_("UserA Last seen"), auto_now=False, auto_now_add=False, null=True, blank=True)
    userb_last_seen = models.DateTimeField(_("UserB Last seen"), auto_now=False, auto_now_add=False, null=True, blank=True)
    last_update = models.DateTimeField(_("Last Changes"), auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        ordering = ['-last_update']


class UserMessage(models.Model):
    message = models.TextField(_("User Message"))
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video = models.ImageField(upload_to='post_images/', storage=VideoMediaCloudinaryStorage(), null=True, blank=True)
    chat = models.ForeignKey(UserChat, verbose_name=_("Chat Node"), on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, verbose_name=_("Reciever"), on_delete=models.CASCADE, related_name="Reciever")
    sender = models.ForeignKey(UserProfile, verbose_name=_("Sender"), on_delete=models.CASCADE, related_name="Sender")
    created = models.DateTimeField(_("Created On"), auto_now=False, auto_now_add=True)
    is_deleted = models.BooleanField(_("Is Deleted"), default=False)
    is_viewed = models.BooleanField(_("Is Viewed"), default=False)

    class Meta:
        ordering = ['created']
