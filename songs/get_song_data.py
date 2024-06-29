from datasets import load_dataset
import os
import pandas as pd
import json

ds = load_dataset("zsoltardai/spotify-tracks", split="train")
print(ds)
os.makedirs('../data/songs', exist_ok=True)
ds.to_json("../data/songs/song_train.json", index=False)
# ds.to_csv("../data/songs/song_train.csv")
""" for split in ds.keys():
    df = ds[split].to_pandas()
    df.to_json(f'../data/songs/song_{split}.json', index=False)

df = df.sample(frac=1).reset_index(drop=True)
df = df.head(1000)

for i in df.index:
    file = open(f"../data/songs/{df.loc[i, "artist"]}-{df.loc[i, "song"]}", "w")
    file.write(f"{df.loc[i, "cleaned_text"]}")
    file.close() """