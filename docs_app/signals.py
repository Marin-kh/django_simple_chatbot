from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Document
from .utils import vector_store, text_splitter
from langchain_core.documents import Document as LangChainDocument

@receiver(post_save, sender=Document)
def update_vector_on_save(sender, instance, **kwargs):
    # حذف تیکه‌های قبلی
    existing_ids = [id_str for id_str in vector_store._collection.get()['ids'] if id_str.startswith(f"{instance.id}_")]
    if existing_ids:
        vector_store.delete(ids=existing_ids)

    langchain_doc = LangChainDocument(
        page_content=instance.text,
        metadata={"title": instance.title, "source": f"doc_{instance.id}", "id": instance.id}
    )
    splits = text_splitter.split_documents([langchain_doc])
    ids = [f"{instance.id}_{i}" for i in range(len(splits))]
    vector_store.add_documents(splits, ids=ids)

    print(f"Document {instance.id} saved/updated - {len(splits)} chunks added")

@receiver(post_delete, sender=Document)
def update_vector_on_delete(sender, instance, **kwargs):
    existing_ids = [id_str for id_str in vector_store._collection.get()['ids'] if id_str.startswith(f"{instance.id}_")]
    if existing_ids:
        vector_store.delete(ids=existing_ids)
    print(f"Document {instance.id} deleted - chunks removed")