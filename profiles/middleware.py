from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from .models import UserProfile


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        if isinstance(request.user, AnonymousUser):
            pass
        else:
           current_user = self.fetch_current_user(request)
           current_user.last_seen = timezone.now()
           current_user.save()
        return None 
    
    def fetch_current_user(self, request):
       return UserProfile.objects.get(user=request.user)