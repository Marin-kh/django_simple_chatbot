from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from langchain_core.vectorstores import InMemoryVectorStore

from .models import Document

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LangChainDocument



def get_langchain_doc(doc):
    return LangChainDocument(
        page_content=doc.text,
        metadata={
            "title": doc.title,
            "source": f"doc_{doc.id}",
            "id": doc.id
        }
    )

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vector_store = InMemoryVectorStore(embeddings)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=300,
    length_function=len,
    is_separator_regex=False,
    separators=[
        "\n\n",
        "\n",
        "۔ ",
        ".",
        "! ",
        "? ",
        " ",
        ""
    ]
)

docs = Document.objects.all()

for doc in docs:
    langchain_doc = get_langchain_doc(doc)
    splits = text_splitter.split_documents([langchain_doc])
    print("************************")
    for s in splits:
        print("___________")
        print(s)
    print("************************")

    ids = [f"{doc.id}_{i}" for i in range(len(splits))]
    vector_store.add_documents(splits, ids=ids)


print("VECTOR STORE ID (signals):", id(vector_store))



@receiver(post_save, sender=Document)
def update_vector_on_save(sender, instance, **kwargs):
    vector_store.delete(ids=[str(instance.id)])

    langchain_doc = LangChainDocument(
        page_content=instance.text,
        metadata={"title": instance.title, "source": f"doc_{instance.id}", "id": instance.id}
    )
    splits = text_splitter.split_documents([langchain_doc])

    ids = [f"{instance.id}_{i}" for i in range(len(splits))]
    vector_store.add_documents(splits, ids=ids)

    print("update_vector_on_save executed - New chunks added for doc", instance.id)


@receiver(post_delete, sender=Document)
def update_vector_on_delete(sender, instance, **kwargs):
    vector_store.delete(ids=[str(instance.id)])
    print("update_vector_on_delete executed - Chunks removed for doc", instance.id)

