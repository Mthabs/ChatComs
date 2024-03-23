from django.db.models import Q
from .models import UserProfile

def search_user_profile(query):
    # Define a query using Q objects to search across multiple fields
    search_query = Q(user__username__icontains=query) | \
                   Q(user__email__icontains=query) | \
                   Q(first_name__icontains=query) | \
                   Q(last_name__icontains=query)

    # Retrieve user profiles matching the search query
    user_profiles = UserProfile.objects.filter(search_query)

    return user_profiles