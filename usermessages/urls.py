from django.urls import path
from . import views

urlpatterns = [
    path('receipients/', views.HandleChatView.as_view(), name="message-recipient"),
    path('<int:fk>/', views.HandleMessageView.as_view(), name="message-list-create"),
    path('add/person/<int:uid>/', views.HandleChatView.as_view(), name="create-chat"),
    path('detail/<int:pk>/', views.MessageUpdateView.as_view(), name="message-update")
]
