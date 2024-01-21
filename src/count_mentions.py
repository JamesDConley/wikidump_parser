# TODO : Test
import argparse
import os
import sys
from tqdm import tqdm
import pandas as pd
from pandarallel import pandarallel
sys.path.append("../src")

import wikitextparser as wtp

def extract_article_names(wikitext):
    # Parse the Wikitext using wikitextparser
    parsed = wtp.parse(str(wikitext))

    # Initialize a list to store article names
    article_names = []

    # Extract article names from links
    for link in parsed.wikilinks:
        article_name = link.title.strip()
        article_names.append(article_name)
    
    return article_names

def count_mentions(input_csv, output_csv, ignore_dupes=False, chunk_size=500000):
    chunk_iter = pd.read_csv(input_csv, chunksize=chunk_size, usecols=["Article Name", "Article Text"])
    first_chunk = True
    assert not os.path.exists(output_csv)
    for chunk in tqdm(chunk_iter):
        chunk['mentions'] = chunk['Article Text'].parallel_apply(extract_article_names) # apply function to each chunk
        if ignore_dupes:
            chunk["mentions"] = chunk["mentions"].parallel_apply(lambda x : list(set(x)))
        chunk[["Article Name", "mentions"]].to_csv(output_csv, mode='a', header=first_chunk, index=None)
        first_chunk = False

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Find mentions in a Wikipedia dump")

    parser.add_argument(
        "input_csv",
        type=str,
        help="Path to the input CSV file containing data for finding mentions in Wikipedia"
    )

    parser.add_argument(
        "output_csv",
        type=str,
        help="Path to the output CSV file to save the results"
    )

    parser.add_argument(
        "--n_workers",
        "-n",
        type=int,
        help="Number of processes to use in parallel",
        default=2
    )
    
    args = parser.parse_args()
    pandarallel.initialize(shm_size_mb=10000, nb_workers=args.n_workers, progress_bar=False)
    count_mentions(args.input_csv, args.output_csv)