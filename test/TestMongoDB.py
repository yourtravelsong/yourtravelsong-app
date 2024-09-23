import logging
import os
import unittest
import certifi
from dotenv import load_dotenv
from pymongo.cursor import Cursor
from pymongo.mongo_client import MongoClient
from config import TestArguments

logger = logging.getLogger(__name__)

class TestDatabases(unittest.TestCase):

    def setUp(self):
        self.argument = TestArguments()
        logging.basicConfig(level=logging.getLevelName(self.argument.log_level))

        if os.getenv("MONGODB_CONNECTION_STRING") is None and os.path.exists(self.argument.env_file):
            load_dotenv(self.argument.env_file)

        assert os.getenv("MONGODB_CONNECTION_STRING") is not None, "MONGODB_CONNECTION_STRING is None"
        self.mongo_uri = os.getenv("MONGODB_CONNECTION_STRING")
        self.isRemote = not "127.0.0.1" in self.mongo_uri and not "localhost" in self.mongo_uri

    def testRetrieveAll(self):

        self.assertTrue(self.mongo_uri is not None)

        client = MongoClient(self.mongo_uri)
        collectionSongsOriginal = client.get_database('yts_db').get_collection('songs_original')

        self.assertTrue(collectionSongsOriginal is not None)

        countDocs = collectionSongsOriginal.count_documents({})
        logger.info(f"Count of documents {countDocs}")
        self.assertTrue(countDocs > 50000 and countDocs < 60000, "Count of documents is not correct")

    def testQueryMongoDB(self):

        self.helperTestQueryMongoDB(isRemote=self.isRemote)


    def helperTestQueryMongoDB(self, isRemote):

        self.assertTrue(self.mongo_uri is not None)
        client = self.getClient(isRemote)
        collectionSongsOriginal = client.get_database('yts_db').get_collection('songs_original')
        result: Cursor = collectionSongsOriginal.find({"artist": "Zwan"})
        print("Result ", result.collection)
        self.assertTrue(result is not None)
        self.assertTrue(result.collection.count_documents({}) > 0)
        ## Cursor to list
        resultList = list(result)
        songName = "Desire".lower()
        print("Result list ", resultList)
        filterSongs = [aSong for aSong in resultList if aSong["song"].lower() == songName]
        print("Filter songs ", filterSongs)
        self.assertTrue(filterSongs is not None)
        self.assertTrue(len(filterSongs) > 0)

    def getClient(self, isRemote):
        if isRemote:
            logger.info(
                "Using remote connection: remember to add your IP address in the MongoDB Atlas site: cloud.mongodb.com/")
            client = MongoClient(self.mongo_uri, tlsCAFile=certifi.where())
        else:
            client = MongoClient(self.mongo_uri)
        return client


    def testPingMongoDB(self):
            client = self.getClient(isRemote=self.isRemote)
            try:
                r = client.admin.command('ping')
                self.assertTrue("ok" in r)
            except Exception as e:
                print(e)
                self.fail("Could not connect to MongoDB Atlas")

if __name__ == '__main__':
    unittest.main()
