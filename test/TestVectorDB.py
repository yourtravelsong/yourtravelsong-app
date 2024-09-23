import logging
import unittest

from llama_index.core import VectorStoreIndex
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone
from dotenv import load_dotenv
import os
import logging
from config import TestArguments

logger = logging.getLogger(__name__)

class VectorDBTest(unittest.TestCase):

    def setUp(self):
        self.argument = TestArguments()
        logging.basicConfig(level=logging.getLevelName(self.argument.log_level))

        if os.getenv("PINECONE_API_KEY") is None and os.path.exists(self.argument.env_file):
            load_dotenv(self.argument.env_file)

        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        assert self.PINECONE_API_KEY is not None, "PINECONE_API_KEY is None"
        self.embed_model = os.getenv("embeddings_name")
        assert self.embed_model is not None, "huggingface_embedding_name is None"

        print(f"Embed model {self.embed_model}")
        self.index_name = os.getenv("VectorStoreName")
        assert self.index_name is not None, "VectorStoreName is None"

    def test_Pinecone(self):

        self.assertIsNotNone(self.PINECONE_API_KEY)
        pc = Pinecone(api_key=self.PINECONE_API_KEY)
        logger.debug(f"Indexes {pc.list_indexes().names()}")
        self.assertTrue(len(pc.list_indexes().names()) > 0)
        pinecone_index = pc.Index(pc.list_indexes().names()[0])
        self.assertIsNotNone(pinecone_index)

    def testQueryPineconeIndex(self):
        embed_model = HuggingFaceEmbedding(model_name=self.embed_model)

        pc = Pinecone( api_key=self.PINECONE_API_KEY )

        pinecone_index = pc.Index(self.index_name)

        vector_store = PineconeVectorStore(pinecone_index=pinecone_index, embed_model=embed_model)

        vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embed_model)

        retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=5, embed_model=embed_model)

        result = retriever.retrieve("San Francisco")

        self.assertTrue(len(result) > 0)
        self.assertEqual(len(result), 5)

        for aResult in result:
            logger.debug("-----")
            logger.debug(f"{len(aResult.embedding)}  {aResult.score} {aResult.metadata['file_name']}")
            self.assertTrue(aResult.score > 0)

if __name__ == '__main__':
    unittest.main()
