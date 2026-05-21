from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from django_eventstream.channelmanager import DefaultChannelManager
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()

from .models import Chat


def get_user_from_token(token_string):
    try:
        token = AccessToken(token_string)
        return User.objects.get(id=token['user_id'])
    except (InvalidToken, TokenError, User.DoesNotExist):
        return None


class ChatChannelManager(DefaultChannelManager):
    def can_read_channel(self, user, channel):
        if not user or not user.is_authenticated:
            return False

        if not channel.startswith("chat-"):
            return False

        try:
            chat_id = int(next(reversed(channel.split("chat-"))))

        except Exception as e:
            return False

        return Chat.objects.filter(id=chat_id, user=user).exists()

    def get_anonymous_channels(self, request, channels):
        if not (token := request.GET.get('token')):
            return []

        if not (user := get_user_from_token(token_string=token)):
            return []

        request.user = user
        request._cached_user = user

        return [channel for channel in channels if self.can_read_channel(user, channel)]
