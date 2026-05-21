from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView

from chat.models import Chat, Message, Document
from chat.serializers import ChatsSerializer, NewChatSerializer, MessageSerializer, MessageSentSerializer

User = get_user_model()


class Chats(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatsSerializer

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)


class CreateChat(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NewChatSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data.get('title')
        original_title = title
        counter = 1

        while Chat.objects.filter(title=title).exists():
            title = f"{original_title} ({counter})"
            counter += 1

        chat = Chat.objects.create(user=request.user, title=title,
                                   **{key: value for key, value in serializer.validated_data.items() if key != "title"})

        return Response(data={"data": "chat created", "title": chat.title, 'id': chat.id},
                        status=status.HTTP_201_CREATED)


class SendMessage(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        chat_id = self.kwargs.get('chat_id')

        try:
            chat = Chat.objects.get(id=chat_id, user=request.user)
        except Chat.DoesNotExist:
            return Response(data={'error': 'Chat not found'}, status=404)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data.get('text', '').strip()

        # if not chat.temporary:
        message = Message.objects.create(chat=chat, role=Message.RoleChoice.USER, text=text or None)

        if files := serializer.validated_data.get('files', []):
            for file in files:
                Document.objects.create(user=request.user, chat=chat, message=message, file=file, file_name=file.name,
                                        file_size=file.size)

        # start_stream_thread(chat=chat, user_text=text, save_to_db=not chat.temporary)

        return Response(data={'status': 'streaming started'}, status=200)


class ReadMessage(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSentSerializer

    def get_queryset(self):
        chat_id = self.kwargs["chat_id"]

        return (Message.objects.filter(chat_id=chat_id, chat__user=self.request.user).select_related("chat").
                prefetch_related("documents").order_by("time"))
