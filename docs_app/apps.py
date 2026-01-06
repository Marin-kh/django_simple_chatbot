from django.apps import AppConfig
import threading
from langchain_core.documents import Document as LangChainDocument


class DocsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'docs_app'

    def ready(self):
        import docs_app.signals

        def populate_initial():
            from .models import Document
            from .utils import vector_store, text_splitter

            docs = Document.objects.all()
            for doc in docs:

                new_doc = [LangChainDocument(page_content=doc.text, metadata={"title": doc.title, "source": f"doc_{doc.id}", "id": doc.id})]
                splits = text_splitter.split_documents(new_doc)
                ids = [f"{doc.id}_{i}" for i in range(len(splits))]

                print("\nAll splits:\n")
                for i, split in enumerate(splits):
                    print(f"split {i}:\n{split}\n")

                vector_store.add_documents(documents=splits, ids=ids)
                print(f"Initial load: Document {doc.id} - {len(splits)} chunks added")

            print("Initial vector_store population completed!")


        threading.Thread(target=populate_initial, daemon=True).start()