from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.retrievers import VectorIndexRetriever

from pinecone import Pinecone, PodSpec

from embeddings.config import settings



class PineconeRpository:
    def __init__(self):
        self.api_key = settings.PINECONE_API_KEY
        self.embed_model = MistralAIEmbedding(api_key=settings.MISTRAL_API_KEY)
        self.pc = Pinecone(api_key=self.api_key)
        self.documents = self.get_documents()
    
    def get_documents(
            self, 
            dociments_path:str="data/cities"
        ):
        return SimpleDirectoryReader(dociments_path).load_data()

    def create_index(
            self, 
            index_name:str = 'cities'
        ):
        if index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=index_name, 
                dimension=1024, 
                metric='cosine',
                spec=PodSpec(
                    environment="gcp-starter"
                )
            )

    def load_documents(
            self, index_name
        ):
        pinecone_index = self.pc.Index(index_name)
        vectordb = PineconeVectorStore(pinecone_index=pinecone_index)
        storage_context = StorageContext.from_defaults(vector_store=vectordb)
        index = VectorStoreIndex.from_documents(
            self.documents, 
            storage_context=storage_context, 
            embed_model=self.embed_model)
        return index
    
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