from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.embeddings.openai import OpenAIEmbedding
# from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama

import os

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# embed_model = OpenAIEmbedding(api_key=OPENAI_API_KEY)
# llm = OpenAI(api_key=OPENAI_API_KEY)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

documents = SimpleDirectoryReader("../data/cities").load_data()

# PERSIST_DIR = "./storage"

index = VectorStoreIndex.from_documents(documents)
    # store it for later
# index.storage_context.persist(persist_dir=PERSIST_DIR)

query_engine = index.as_query_engine()

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

print(query_engine.query(query))