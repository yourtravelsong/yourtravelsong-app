from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding

from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import get_response_synthesizer, VectorStoreIndex
from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from embeddings.custom_query_engine import RAGQueryEngine
from embeddings.config import settings

llm = MistralAI(api_key=settings.MISTRAL_API_KEY)
embed_model = MistralAIEmbedding(api_key=settings.MISTRAL_API_KEY)

index_name = "cities"


pc = Pinecone(
    api_key=settings.PINECONE_API_KEY
)

pinecone_index = pc.Index(index_name)

# Initialize VectorStore
vector_store = PineconeVectorStore(pinecone_index=pinecone_index, embed_model=embed_model)

vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embed_model)

retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=5, embed_model=embed_model)

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
