from llama_index.llms.mistralai import MistralAI
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import get_response_synthesizer
from embeddings.custom_query_engine import RAGQueryEngine
from embeddings.config import settings
from dal.dal import MongoRepository
from embeddings.pinecone_repo import PineconeRpository

class QueryDispatcher:
    def __init__(self):
        self.llm = MistralAI(
            api_key=settings.MISTRAL_API_KEY
        )
        self.pinecone_repo = PineconeRpository()
        self.mongo_repo = MongoRepository(
                                db_name="sample_mflix",
                                collection_name="songs"
                            )

        self.synthesizer = get_response_synthesizer(
            response_mode="compact", llm=self.llm
        )
        
        self.song_lyrics: str = ''
        self.retriever: VectorIndexRetriever = None
        self.query:str = ''
        
    def get_song_lyrics(self, song:str):
        query = {"song": song}
        response = self.mongo_repo.find_one(query)
        self.song_lyrics = response.get("cleaned_text")

    def compose_query(self, song:str):
        self.get_song_lyrics(song)
        self.query = f"""
            What cities do you think someone listening to 
            the following song would like to visit based on 
            the sentiment of the song. Base your answers only 
            on cities that appear in the context?.
            I want you to return a json response such that ("song": "song_name", 
            "cities": ["city1", "city2", "city3"], "sentiment": ["sentiment1", 
            "sentiment2", "sentiment3]) -> {self.song_lyrics}
            """
    
    def get_response(self, song:str):
        self.compose_query(song)
        self.retriever = self.pinecone_repo.get_retriever("cities")
        query_engine = RAGQueryEngine(
            retriever=self.retriever, 
            response_synthesizer=self.synthesizer
        )
        response = query_engine.query(self.query)
        return response
