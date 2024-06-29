from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.llms.mistralai import MistralAI

from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.retrievers import BaseRetriever, VectorIndexRetriever
from llama_index.core import get_response_synthesizer
from llama_index.core.response_synthesizers import BaseSynthesizer
from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from config import settings
import os


class RAGQueryEngine(CustomQueryEngine):
    """RAG Query Engine."""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer

    def custom_query(self, query_str: str):
        nodes = self.retriever.retrieve(query_str)
        response_obj = self.response_synthesizer.synthesize(query_str, nodes)
        return response_obj
    



MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

llm = MistralAI(api_key=MISTRAL_API_KEY)

index_name = "cities"


pc = Pinecone(
    api_key=settings.PINECONE_API_KEY
)

pinecone_index = pc.Index(index_name)

# Initialize VectorStore
vector_store = PineconeVectorStore(pinecone_index=pinecone_index, llm=llm)

vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store, llm=llm)

retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=5, llm=llm)

query = """
    What cities do you think someone listening to the following song would like to visit based on the sentiment of the song. Base your answers only on cities that appear in the context? explain briefly why.
Imagine there's no heaven
It's easy if you try
No hell below us
Above us only sky
Imagine all the people living for today

Imagine there's no countries
It isn't hard to do
Nothing to kill or die for
And no religion too
Imagine all the people living life in peace, you

You may say I'm a dreamer
But I'm not the only one
I hope some day you'll join us
And the world will be as one

Imagine no possessions
I wonder if you can
No need for greed or hunger
A brotherhood of man
Imagine all the people sharing all the world, you

You may say I'm a dreamer
But I'm not the only one
I hope some day you'll join us
And the world will be as one
"""

synthesizer = get_response_synthesizer(response_mode="compact", llm=llm)
query_engine = RAGQueryEngine(
    retriever=retriever, 
    response_synthesizer=synthesizer
)

response = query_engine.query(query)

print(str(response))
