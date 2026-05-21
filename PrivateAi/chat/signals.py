# from django.db.models.signals import post_delete, pre_delete
# from django.dispatch import receiver
# from .models import Chat, Document
#
#
# @receiver(pre_delete, sender=Chat)
# def delete_chat_documents(sender, instance, **kwargs):
#     """
#     Fires BEFORE a Chat is deleted.
#     Cleans up files + pgvector embeddings for all documents in this chat.
#     pre_delete (not post_delete) because we need Document records
#     still in DB to read collection_name and vector_doc_ids.
#     """
#     if not instance.temporary:
#         return
#
#     for document in instance.document_set.all():
#         _delete_document_assets(document)
#
#
# @receiver(pre_delete, sender=Document)
# def delete_document_assets(sender, instance, **kwargs):
#     """
#     Fires whenever any Document is deleted individually.
#     Handles the file + embedding cleanup regardless of how the delete was triggered.
#     """
#     _delete_document_assets(instance)
#
#
# def _delete_document_assets(document):
#     """Shared cleanup logic: pgvector chunks + physical file."""
#     import os
#     from documents.embeddings import get_vectorstore
#
#     # 1. Delete embeddings from pgvector
#     if document.vector_doc_ids and document.collection_name:
#         try:
#             store = get_vectorstore(document.collection_name)
#             store.delete(ids=document.vector_doc_ids)
#         except Exception:
#             pass   # log this in production
#
#     # 2. Delete physical file from disk
#     if document.file and document.file.name:
#         if os.path.exists(document.file.path):
#             os.remove(document.file.path)