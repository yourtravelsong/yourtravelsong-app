from llama_index.llms.mistralai import MistralAI
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import get_response_synthesizer
from custom_query_engine import RAGQueryEngine
from config import settings
from dal.dal import MongoRepository
from pinecone_repo import PineconeRpository

class QueryDispatcher:
    def __init__(self):
        self.llm = MistralAI(
            api_key=settings.MISTRAL_API_KEY)
        self.pc = PineconeRpository(
            api_key=settings.PINECONE_API_KEY)
        self.mongo_repo = MongoRepository(
                                db_name="sample_mflix",
                                collection_name="songs"
                            )

        self.synthesizer = get_response_synthesizer(
            response_mode="compact", llm=self.llm
        )
        
        self.song_lyrics: str = ''
        self.retriever: VectorIndexRetriever = None
        self.query_engine: RAGQueryEngine = None
        self.query:str = ''
        
    def get_song_lyrics(self, song:str):
        query = {"song": song}
        self.song_lyrics = self.mongo_repo.find_one(query)

    def get_retriever(self, index_name:str):
        self.retriever = self.pc.get_retriever(index_name)

    def compose_query(self, song:str):
        self.get_song_lyrics(song)
        self.query = f"""
            What cities do you think someone listening to 
            the following song would like to visit based on 
            the sentiment of the song. Base your answers only 
            on cities that appear in the context?.
            I want you to return a json response such that ("song": "song_name", 
            "cities": ["city1", "city2", "city3"], "sentiment": ["sentiment1", 
            "sentiment2", "sentiment3]) {self.song_lyrics}
            """.format(self.song_lyrics)
    
    def get_response(self):
        self.compose_query()
        self.retriever = self.get_retriever("cities")
        self.query_engine = RAGQueryEngine(
            retriever=self.retriever, 
            response_synthesizer=self.synthesizer
        )
        response = self.query_engine.custom_query(self.query)
        return response
