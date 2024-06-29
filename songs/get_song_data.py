from datasets import load_dataset
import os
import pandas as pd

ds = load_dataset("zsoltardai/spotify-tracks")
os.makedirs('../data/songs', exist_ok=True)
for split in ds.keys():
    df = ds[split].to_pandas()
    df.to_csv(f'../data/songs/song_{split}.csv', index=False)
