import uuid

from django.db import models
from django.conf import settings
from pgvector.django import VectorField


def original_upload_path(instance, filename):
    return f'{instance.user.id}/{instance.chat.id}/{uuid.uuid4()}_{filename}'


class Chat(models.Model):
    class RetrievalScope(models.TextChoices):
        GLOBAL = 'global', 'Global (shared + user docs)'
        SESSION = 'session', 'Session (only this chat uploads)'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats')

    title = models.CharField(max_length=200)
    # temporary = models.BooleanField(default=False)
    retrieval_scope = models.CharField(max_length=10, choices=RetrievalScope.choices, default=RetrievalScope.GLOBAL)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    class RoleChoice(models.TextChoices):
        USER = 'user', 'User'
        ASSISTANT = 'assistant', 'Assistant'
        SYSTEM = 'system', 'System'

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=RoleChoice.choices)
    text = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    edited_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["time"]

    def __str__(self):
        return f'[{self.role}] {self.text[:60] if self.text else ""}'


class Document(models.Model):
    class ProcessStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        DONE = 'done', 'Done'
        FAILED = 'failed', 'Failed'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='documents')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='documents')

    file_size = models.PositiveBigIntegerField()
    file = models.FileField(upload_to=original_upload_path)
    file_name = models.CharField(max_length=255, null=True, blank=True)

    process_status = models.CharField(max_length=15, choices=ProcessStatus.choices, default=ProcessStatus.PENDING)

    collection_name = models.CharField(max_length=255, blank=True)
    vector_doc_ids = models.JSONField(default=list)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name or str(self.id)


class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')

    content = models.TextField(null=True, blank=True)
    vector_id = models.UUIDField(unique=True, null=True, blank=True)
    embedding = VectorField(dimensions=1536, null=True, blank=True)
    chunk_index = models.PositiveIntegerField()

    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['chunk_index']
        constraints = [
            models.UniqueConstraint(fields=['document', 'chunk_index'], name='unique_chunk_per_document')
        ]

    def __str__(self):
        return f'Chunk {self.chunk_index} — {self.document.file_name}'
