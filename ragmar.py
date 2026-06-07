from langchain_community.vectorstores import (
    FAISS
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

embeddings = HuggingFaceEmbeddings(

    model_name=
    "sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(

    "market_db",

    embeddings,

    allow_dangerous_deserialization=True
)

def retrieve_market(query):

    docs = db.similarity_search(

        query,

        k=10
    )

    context = []

    for doc in docs:

        context.append(
            doc.page_content
        )

    return context