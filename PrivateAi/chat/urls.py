import django_eventstream
from django.urls import path, include

from chat.views import Chats, CreateChat, SendMessage, ReadMessage

urlpatterns = [
    path("chats/", Chats.as_view(), name="chats"),
    path("chats/create/", CreateChat.as_view(), name="create_chat"),
    path("chats/<int:chat_id>/message/", SendMessage.as_view(), name="send_message"),
    path("chats/<int:chat_id>/messages/", ReadMessage.as_view(), name="read_message"),
    path('chats/<int:chat_id>/stream/', include(django_eventstream.urls),
         {"format-channels": ["chat-{chat_id}"]}, name="stream"),
]
