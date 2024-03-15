from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    IMAGE_FILTER_CHOICES = [
        ('normal', 'Normal'),
        ('black_and_white', 'Black and White'),
        ('sepia', 'Sepia'),
        ('vintage', 'Vintage'),
        ('grayscale', 'Grayscale'),
        ('warm', 'Warm Tone'),
        ('cool', 'Cool Tone'),
        ('invert', 'Invert Colors'),
        ('blur', 'Blur'),
        ('sharpen', 'Sharpen'),
    ]
    header = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post_picture = models.ImageField(upload_to='post_images/', null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image_filter = models.CharField(
        max_length=32,
        choices=IMAGE_FILTER_CHOICES,
        default='normal',
        blank=True,
        null=True
    )
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
