from datasets import load_dataset
import os
import pandas as pd

ds = load_dataset("zsoltardai/spotify-tracks")
os.makedirs('../data/songs', exist_ok=True)
for split in ds.keys():
    df = ds[split].to_pandas()
    df.to_csv(f'../data/songs/song_{split}.csv', index=False)

df = df.sample(frac=1).reset_index(drop=True)
df = df.head(1000)

for i in df.index:
    file = open(f"../data/songs/{df.loc[i, "artist"]}-{df.loc[i, "song"]}", "w")
    file.write(f"{df.loc[i, "cleaned_text"]}")
    file.close()