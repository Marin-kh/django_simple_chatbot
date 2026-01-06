from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Document
from .vectorstore import rebuild_vector_store

@receiver(post_save, sender=Document)
def on_document_save(sender, instance, **kwargs):
    print("Document saved/updated — rebuilding vector store...")
    rebuild_vector_store()

@receiver(post_delete, sender=Document)
def on_document_delete(sender, instance, **kwargs):
    print("Document deleted — rebuilding vector store...")
    rebuild_vector_store()