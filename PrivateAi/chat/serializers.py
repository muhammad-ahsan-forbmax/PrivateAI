from rest_framework import serializers

from chat.models import Chat, Message


class ChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class NewChatSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    temporary = serializers.BooleanField(default=False)
    retrieval_scope = serializers.ChoiceField(choices=Chat.RetrievalScope.choices, default=Chat.RetrievalScope.GLOBAL,
                                              required=False)


class MessageSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, allow_blank=True)
    files = serializers.ListField(child=serializers.FileField(), required=False, max_length=5)

    def validate(self, attrs):
        text = attrs.get('text', '').strip()
        files = attrs.get('files', [])

        if not text and not files:
            raise serializers.ValidationError('You must provide either text or at least one file.')

        return attrs


class MessageSentSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["id", "chat", "role", "text", "time", "edited_time", "documents"]

    def get_documents(self, obj):
        return [{
            "id": doc.id,
            "file_name": doc.file_name,
            "file": doc.file.url,
            "size": doc.file_size
        } for doc in obj.documents.all()]
