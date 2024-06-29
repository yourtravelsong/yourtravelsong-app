from dal.dal import MongoRepository
import json

mongo_repo = MongoRepository(
   db_name="sample_mflix",
   collection_name="songs")


with open('data/songs/song_train.json', 'r') as f:
    data = [json.loads(line) for line in f]
    for song in data:
        mongo_repo.insert(song)
        print(song)