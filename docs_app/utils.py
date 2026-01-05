from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vector_store = InMemoryVectorStore(embeddings)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=400,
    length_function=len,
    is_separator_regex=False,
    separators=[
        "\n\n",
        "\n",
        "۔ ",
        ". ",
        " .",
        "!",
        "?",
        "؛ ",
        "، ",
        " ",
    ]
)

print("VECTOR STORE ID (utils):", id(vector_store))