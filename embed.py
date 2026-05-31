from langchain_text_splitters import (
    CharacterTextSplitter
)

from langchain_community.document_loaders import (
    TextLoader
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

import os


# STORE ALL DOCUMENTS
documents = []


# KNOWLEDGE FOLDER PATH
folder_path = r"C:\Users\Admin\Desktop\Acads\Investment suggestor\knowledge"


# CHECK IF FOLDER EXISTS
if not os.path.exists(folder_path):

    print("Knowledge folder not found!")

    exit()


# LOAD ALL TXT FILES
for file in os.listdir(folder_path):

    print(f"FOUND FILE: {file}")

    if file.endswith(".txt"):

        full_path = os.path.join(
            folder_path,
            file
        )

        print(f"LOADING: {full_path}")

        try:

            loader = TextLoader(
                full_path,
                encoding="utf-8"
            )

            loaded_docs = loader.load()

            print(
                f"DOCS LOADED: {len(loaded_docs)}"
            )

            documents.extend(
                loaded_docs
            )

        except Exception as e:

            print(
                f"ERROR LOADING {file}: {e}"
            )


# CHECK DOCUMENT COUNT
print(
    "TOTAL DOCUMENTS:",
    len(documents)
)


# STOP IF NO DOCUMENTS
if len(documents) == 0:

    print(
        "No documents loaded!"
    )

    exit()


# SPLIT DOCUMENTS INTO CHUNKS
text_splitter = CharacterTextSplitter(

    chunk_size=500,

    chunk_overlap=50
)

docs = text_splitter.split_documents(
    documents
)


# CHECK CHUNKS
print(
    "TOTAL CHUNKS:",
    len(docs)
)


# STOP IF NO CHUNKS
if len(docs) == 0:

    print(
        "No chunks created!"
    )

    exit()


# LOAD EMBEDDING MODEL
print(
    "Loading embedding model..."
)

embeddings = HuggingFaceEmbeddings(

    model_name=
    "sentence-transformers/all-MiniLM-L6-v2"
)


# CREATE FAISS DATABASE
print(
    "Creating FAISS database..."
)

db = FAISS.from_documents(

    docs,

    embeddings
)


# SAVE DATABASE
db.save_local(
    "faiss_db"
)


print(
    "FAISS database created successfully!"
)