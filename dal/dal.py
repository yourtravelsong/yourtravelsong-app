from pymongo import MongoClient
from typing import Any, Dict
from dal import config
import certifi

class MongoRepository:
    def __init__(
            self,
            db_name: str, 
            collection_name: str
    ):
        self.client = MongoClient(
            config.settings.MONGODB_CONNETCTION_STRING,
            tlsCAFile=certifi.where()
            )
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def find_one(
            self, 
            query: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.collection.find_one(query)
    
    def find(
            self, 
            query: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.collection.find(query)

    def insert(
            self,
            data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.collection.insert_one(data).inserted_id