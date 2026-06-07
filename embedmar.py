from langchain_core.documents import (
    Document
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from news import (
    get_market_news
)

news = get_market_news()

documents = []

for article in news:

    documents.append(

        Document(

            page_content=
            article["text"]
        )
    )

print(
    "News Articles:",
    len(documents)
)

embeddings = HuggingFaceEmbeddings(

    model_name=
    "sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_documents(

    documents,

    embeddings
)

db.save_local(
    "market_db"
)

print(
    "Market database created successfully!"
)