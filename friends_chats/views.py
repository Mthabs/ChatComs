
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from dj_rest_auth.views import LoginView
from rest_framework.authtoken.models import Token


@api_view()
def root_route(request):
    return Response({
        "message": "Backend Deployment is successful"
    })


class CustomRegisterView(RegisterView):
    """
    Overrided Registeration View to by pass Email Verification
    """
    serializer_class = CustomRegisterSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        return Response(
            {"message": "Account Created successfully", "id":user.id},
            status=status.HTTP_201_CREATED,
        )
    
    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user
    

class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data, context={'request': request})
        if self.serializer.is_valid():
            # Obtain the authenticated user
            user = self.serializer.validated_data['user']
            # Check if the user has an existing token
            token, created = Token.objects.get_or_create(user=user)
            # Optionally, you may want to check the created flag to handle cases
            # where the token already exists for the user
            return Response({'token': token.key})
        else:
            return Response(self.serializer.errors, status=status.HTTP_400_BAD_REQUEST)