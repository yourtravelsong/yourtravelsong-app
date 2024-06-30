from llama_index.llms.mistralai import MistralAI
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import get_response_synthesizer
from embeddings.custom_query_engine import RAGQueryEngine, RAGStringQueryEngine
from embeddings.config import settings
from dal.dal import MongoRepository
from embeddings.pinecone_repo import PineconeRpository
from llama_index.core import PromptTemplate


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
        
    def get_song_lyrics(self, song:str, artist:str):
        query = {"song": song, "artist": artist}
        response = self.mongo_repo.find_one(query)
        self.song_lyrics = response.get("cleaned_text")

    def compose_query(self, song:str, artist:str):
        self.get_song_lyrics(song, artist=artist)
        self.query = f"""
            What cities do you think someone listening to 
            the following song would like to visit based on 
            the sentiment of the song. Base your answers only 
            on cities that appear in the context?.
            I want you to return a json response such that ("song": "song_name", 
            "cities": ["city1", "city2", "city3"], "sentiment": ["sentiment1", 
            "sentiment2", "sentiment3], "reason_why_city1": "reason1")

            song: {song}
            song_lyrics: {self.song_lyrics}
            """
        
        self.prompt = PromptTemplate(
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and only the context information, with no prior knowledge, "
            "answer the query.\n"
            "Query: {query_str}\n"
            "Answer: "
        )
    
    def get_response(self, song:str, artist:str):
        self.compose_query(song, artist)
        self.retriever = self.pinecone_repo.get_retriever("cities")
        query_engine = RAGStringQueryEngine(
            retriever=self.retriever, 
            response_synthesizer=self.synthesizer,
            llm=self.llm,
            qa_prompt=self.prompt
        )
        response = query_engine.custom_query(self.query)
        return response
