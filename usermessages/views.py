from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from usermessages.models import UserChat, UserMessage
from usermessages.serializers import UserChatCreateSerializer, UserChatGetSerializer, UserMessageCreateSerializer, UserMessageFetchSerializer
from profiles.models import UserProfile


# Create your views here.
class HandleChatView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserChatGetSerializer

    def get(self, request):
        current_user = self.fetch_current_user(request)
        userchat_instances = UserChat.objects.filter(Q(user_a=current_user) | Q(user_b=current_user))
        serializer = self.serializer_class(userchat_instances, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, uid):
        current_user = self.fetch_current_user(request)
        user = self.fetch_user_from_request_data(uid)
        instance = UserChat.objects.filter( Q(user_a=current_user, user_b=user) | Q(user_a=user, user_b=current_user) ).first()
        if not instance:
            instance = UserChat.objects.create(user_a=current_user, user_b=user)
            serializer = UserChatGetSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            serializer = UserChatGetSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

    
    def fetch_current_user(self, request):
        return UserProfile.objects.get(user=request.user)
    
    def fetch_user_from_request_data(self, uid):
        return UserProfile.objects.get(id=uid)
    

class HandleMessageView(APIView):
    serializer_class = UserMessageFetchSerializer
    def get(self, request, fk):
        self.mark_read_to_new_messages(request,fk)
        chat = self.fetch_chat_instance(fk)
        messages = UserMessage.objects.filter(chat=chat)
        serializer = self.serializer_class(messages, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, fk):
        serializer = UserMessageCreateSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message":"Message instance created"}, status=status.HTTP_201_CREATED)
        except Exception as exc:
            return Response({"error": exc}, status=status.HTTP_400_BAD_REQUEST)
        
    def fetch_chat_instance(self, fk):
        return get_object_or_404(UserChat, id=fk)
    
    def mark_read_to_new_messages(self, request, fk):
        chat = self.fetch_chat_instance(fk)
        userprofile = UserProfile.objects.get(user=request.user)
        messages = UserMessage.objects.filter(chat=chat, receiver=userprofile, is_viewed=False)
        for message in messages:
            message.is_viewed = True
            message.save()
        return
        
class MessageUpdateView(APIView):
    def patch(self, request, pk):
        message = self.fetch_message_instance(pk)
        serializer = UserMessageCreateSerializer(instance=message, data=request.data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message":"Message instance updated"}, status=status.HTTP_206_PARTIAL_CONTENT)
        except Exception as exc:
            return Response({"error": str(exc).strip("\n")}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        message = self.fetch_message_instance(pk)
        message.is_deleted=True
        message.save()
        return Response({"message":"Message instance deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    def fetch_message_instance(self, pk):
        return get_object_or_404(UserMessage, id=pk)


    
        

