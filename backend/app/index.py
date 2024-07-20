import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.embeddings.jinaai import JinaEmbedding
from llama_index.llms.groq import Groq
from llama_index.core import Settings

from llama_index.core.callbacks import CallbackManager
from langfuse.llama_index import LlamaIndexCallbackHandler

import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=100)
print(os.environ.get("LANGFUSE_PUBLIC_KEY"))
def query_engine(collection="Milvus_Demo"):
    langfuse_callback_handler = LlamaIndexCallbackHandler(
        public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
        host=os.environ.get("LANGFUSE_URL")
    )
    Settings.callback_manager = CallbackManager([langfuse_callback_handler])
    Settings.llm = Groq(model="llama3-70b-8192", api_key=os.environ.get("GROQ_API_KEY"))
    Settings.embed_model = JinaEmbedding(
        api_key=os.environ.get("JINAAI_API_KEY"),
        #embed_batch_size=768,
        model="jina-embeddings-v2-base-en",
    )

    vector_store = MilvusVectorStore(
        uri=os.environ.get("MILVUS_URL"),
        collection_name=collection,
        overwrite=False,
        enable_sparse=True,
    )
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    return index.as_query_engine(vector_store_query_mode="hybrid", similarity_top_k=5)


async def query_index(query_text):
    loop = asyncio.get_running_loop()
    llm_query_engine = query_engine()
    response = await loop.run_in_executor(executor, llm_query_engine.query, query_text)
    return response