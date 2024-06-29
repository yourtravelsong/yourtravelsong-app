from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore

from pinecone import Pinecone, ServerlessSpec, PodSpec

import os
from config import settings

embed_model = MistralAIEmbedding(api_key=settings.MISTRAL_API_KEY)

pc = Pinecone(
    api_key=settings.PINECONE_API_KEY
)

documents = SimpleDirectoryReader("../data/cities").load_data()


index_name = "cities"

# Now do stuff
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name, 
        dimension=1024, 
        metric='cosine',
        spec=PodSpec(
            environment="gcp-starter"
        )
    )

pinecone_index = pc.Index(index_name)


vectordb = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vectordb)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embed_model)

