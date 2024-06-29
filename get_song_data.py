from datasets import load_dataset
import pandas as pd

ds = load_dataset("zsoltardai/spotify-tracks")
for split in ds.keys():
    df = ds[split].to_pandas()
    df.to_csv(f'song_{split}.csv', index=False)
