from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document as LangChainDocument
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .models import Document


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=300,
)

_vector_store = InMemoryVectorStore(embeddings)


def get_vector_store():
    return _vector_store


def rebuild_vector_store():
    global _vector_store

    _vector_store = InMemoryVectorStore(embeddings)

    docs = Document.objects.all()
    print(f"Rebuilding vector_store with {docs.count()} documents...")

    for doc in docs:
        langchain_doc = LangChainDocument(
            page_content=doc.text,
            metadata={"title": doc.title, "source": f"doc_{doc.id}", "id": doc.id}
        )

        splits = text_splitter.split_documents([langchain_doc])
        ids = [f"{doc.id}_{i}" for i in range(len(splits))]

        _vector_store.add_documents(documents=splits, ids=ids)

        print("\nRetrieved documents:\n")
        for i, split in enumerate(splits):
            print(f"chunk {i+1}:\n{split}\n")

        print(f"Document {doc.id} ({doc.title}) - {len(splits)} chunks added")

    print("Vector store rebuilt successfully!")


rebuild_vector_store()