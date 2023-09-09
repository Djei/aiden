import os
from dotenv import load_dotenv
load_dotenv()

from langchain.embeddings import HuggingFaceEmbeddings
from llama_index import LangchainEmbedding, ServiceContext, StorageContext, load_index_from_storage
from langchain.chat_models import ChatOpenAI
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.index_store import SimpleIndexStore

import chromadb

import logging
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

chroma_client = chromadb.PersistentClient(path="./storage/vector_storage/chromadb/")
chroma_collection = chroma_client.get_or_create_collection("google_calendar_api")
logging.info("Instantiated chroma client")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store, index_store=SimpleIndexStore.from_persist_dir(persist_dir="./storage/index_storage/google_calendar_api/"))
logging.info("Created storage context")
service_context = ServiceContext.from_defaults(
    embed_model=LangchainEmbedding(HuggingFaceEmbeddings())
)
logging.info("Created service context")

index = load_index_from_storage(service_context=service_context, storage_context=storage_context)
logging.info("Created index")

query_engine = index.as_query_engine()
question = "How do you create an event with the google calendar api? Please provide an sample api call."
answer = query_engine.query(question)
logging.info(f"question: {question}")
logging.info(f"answer: {answer}")