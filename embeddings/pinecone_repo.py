from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.retrievers import VectorIndexRetriever
from pinecone import Pinecone, PodSpec
from embeddings.config import Settings

class PineconeRepository:
    def __init__(self):
        settings = Settings()
        self.api_key = settings.PINECONE_API_KEY
        #TODO: Configure the embedding model
        self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        ##self.embed_model = MistralAIEmbedding(api_key=settings.MISTRAL_API_KEY)
        self.pc = Pinecone(api_key=self.api_key)
    
    def get_retriever(
            self, index_name
        ):
        pinecone_index = self.pc.Index(index_name)
        vector_store = PineconeVectorStore(
            pinecone_index=pinecone_index, 
            embed_model=self.embed_model
        )
        vector_index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store, 
            embed_model=self.embed_model)

        return VectorIndexRetriever(
            index=vector_index, 
            similarity_top_k=5, 
            embed_model=self.embed_model
        )