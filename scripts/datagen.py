import logging
import sys

# Uncomment to see debug logs
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.vector_stores.milvus import MilvusVectorStore
from IPython.display import Markdown, display
import textwrap


# load documents
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()

print("Document ID:", documents[0].doc_id)

from llama_index.core import StorageContext
import os


vector_store = MilvusVectorStore(
    dim=1536,
    overwrite=True,
    enable_sparse=True,
    hybrid_ranker="RRFRanker",
    hybrid_ranker_params={"k": 60},
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

query_engine = index.as_query_engine(vector_store_query_mode="hybrid")
response = query_engine.query("What did the author learn?")
print(textwrap.fill(str(response), 100))

response = query_engine.query("What was a hard moment for the author?")
print(textwrap.fill(str(response), 100))