# TODO : Organize file
import os
import argparse
from collections import defaultdict
from copy import deepcopy
import pandas as pd
from tqdm import tqdm

from pandarallel import pandarallel


def split_title(title):
    vals = title.lstrip("[").rstrip("]").split("|")
    vals = [f"[[{val}]]" for val in vals]
    return vals

def get_title(title):
    vals = title.lstrip("[").rstrip("]")
    if "|" in vals:
        vals = vals.split("|")[0]
    return vals

def process_mentions(data):
    return tuple(item for item in eval(data))

def combine_dictionaries(dict_list, ignore_dupes=False):
    combined = dict_list[0]
    for arg in dict_list[1:]:
        for key, value in arg.items():
            if not ignore_dupes:
                combined[key] += value
            else:
                combined[key] += 1
    return combined

def count_frequency(words):
    freq = defaultdict(int)
    for word in words:
        freq[word] += 1
    return freq

def get_args():
    parser = argparse.ArgumentParser(description="Find mentions in a Wikipedia dump")

    parser.add_argument(
        "mention_counts_csv",
        type=str,
        help="Path to the input CSV file containing data for finding mentions in Wikipedia"
    )

    parser.add_argument(
        "output_csv",
        type=str,
        help="Path to the output CSV file to save the results"
    )
    parser.add_argument(
        "--ignore_dupes",
        action="store_true",
        help="If provided, mention counts will be the number of other articles that mention the current article. Otherwise it is the total count of mentions across all articles- including duplicates within the same article."
    )

    parser.add_argument(
        "--n_workers",
        "-n",
        type=int,
        help="Number of processes to use in parallel",
        default=2
    )
    
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    
    tqdm.pandas()
    args = get_args()
    pandarallel.initialize(shm_size_mb=10000, nb_workers=args.n_workers, progress_bar=False)
    mention_df = pd.read_csv(args.mention_counts_csv, usecols=["Article Name", "mentions"], chunksize=50000)
    cumulative_counts = defaultdict(int)
    assert not os.path.exists(args.output_csv), f"Output path would be overwritten!"
    for chunk in tqdm(mention_df):
        mentions = chunk["mentions"].parallel_apply(process_mentions)
        all_counts = combine_dictionaries(mentions.apply(count_frequency).values)
        cumulative_counts = combine_dictionaries([cumulative_counts, all_counts], ignore_dupes=args.ignore_dupes)
        del chunk

    values = []
    keys = []
    for key, value in tqdm(cumulative_counts.items()):
        keys.append(key)
        values.append(value)

    tmp_df = pd.DataFrame({"article" : keys, "mentions" : values})
    tmp_df.sort_values("mentions", inplace=True, ascending=False)
    tmp_df.to_csv(args.output_csv, index=None)