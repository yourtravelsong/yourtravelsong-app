import logging

from llama_index.llms.mistralai import MistralAI
from llama_index.core.retrievers import VectorIndexRetriever
from embeddings.config import Settings
from embeddings.custom_query_engine import RAGStringQueryEngine
from dal.dal import MongoRepository
from embeddings.pinecone_repo import PineconeRepository
from llama_index.core import PromptTemplate


logger = logging.getLogger(__name__)

prompt = PromptTemplate(
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and only the context information, with no prior knowledge, "
    "answer the query.\n"
    "Query: {query_str}\n"
    "Answer: "
)


class QueryDispatcher:

    def __init__(self):

        self.settings = Settings()
        ## TODO: configure llm to be used by the response synthesizer
        self.llm = MistralAI(
            api_key=self.settings.MISTRAL_API_KEY
        )
        self.pinecone_repo = PineconeRepository()
        self.mongo_repo = MongoRepository(
            db_name=self.settings.mongodb_name,
            collection_name=self.settings.mongodb_collection_name)

        #self.synthesizer = get_response_synthesizer(
        #    response_mode="compact", llm=self.llm
        #)

        self.retriever: VectorIndexRetriever = None

    def get_response(self, song:str, artist:str):
        aQuery = self.__compose_query(song, artist)
        self.retriever = self.pinecone_repo.get_retriever(self.settings.VectorStoreName)
        query_engine = RAGStringQueryEngine(
            retriever=self.retriever,
            #response_synthesizer=self.synthesizer,
            llm=self.llm,
            qa_prompt=prompt
        )
        response = query_engine.custom_query(aQuery)
        return response

    def __get_song_lyrics(self, song:str, artist:str):
        query = {"song": song, "artist": artist}
        response = self.mongo_repo.find_one(query)
        logger.debug("Response From Mongo: ", response)
        return response.get("cleaned_text")

    def __compose_query(self, song:str, artist:str):
        song_lyrics = self.__get_song_lyrics(song, artist=artist)
        query = f"""
            What cities do you think someone listening to 
            the following song would like to visit based on 
            the sentiment of the song. Base your answers only 
            on cities that appear in the context?.
            I want you to return a json response such that ("song": "song_name", 
            "cities": ["city1", "city2", "city3"], "sentiment": ["sentiment1", 
            "sentiment2", "sentiment3], "reasons_why": dict("city1":"reason_why_city1", 
                                                        "city2":"reason_why_city2"
                                                        "city3":"reason_why_city3"))

            song: {song}
            song_lyrics: {song_lyrics}
            """
        return query
        

    
