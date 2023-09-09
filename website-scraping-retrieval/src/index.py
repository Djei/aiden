import os
from dotenv import load_dotenv
load_dotenv()

from langchain.embeddings import HuggingFaceEmbeddings
from llama_index import LangchainEmbedding, ServiceContext, StorageContext, SimpleDirectoryReader, GPTVectorStoreIndex
from langchain.chat_models import ChatOpenAI
from llama_index.vector_stores import ChromaVectorStore

import chromadb

import logging
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

chroma_client = chromadb.PersistentClient(path="./storage/vector_storage/chromadb/")
chroma_collection = chroma_client.get_or_create_collection("google_calendar_api")
logging.info("Instantiated chroma client")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
logging.info("Created storage context")
service_context = ServiceContext.from_defaults(
    embed_model=LangchainEmbedding(HuggingFaceEmbeddings())
)
logging.info("Created service context")

documents = SimpleDirectoryReader("./data/clean/google_calendar_api/").load_data()
logging.info("Loaded documents")

index = GPTVectorStoreIndex.from_documents(documents=documents, storage_context=storage_context, service_context=service_context, show_progress=True)
logging.info("Created index")

index.set_index_id("gptvector_google_calendar_api")
index.storage_context.persist('./storage/index_storage/google_calendar_api/')
logging.info("Saved index")