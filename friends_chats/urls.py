from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import root_route, CustomRegisterView, CustomLoginView, CustomPasswordChange

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version="v1",
        description="Your API description",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@friends.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", root_route),
    path("admin/", admin.site.urls),
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("auth/register/", CustomRegisterView.as_view(), name="register-view"),
    path("auth/token/", CustomLoginView.as_view(), name="Authentication-token"),
    path("auth/password/change/", CustomPasswordChange.as_view(), name="password change"),
    path("friends/", include("friends.urls")),
    path("profile/", include("profiles.urls")),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("post/", include("posts.urls")),
]
