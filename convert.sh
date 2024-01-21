#!/bin/bash
# Exit on error 
set -e
python3 src/gen_csv.py -i $1 -o data/output/base_dump.csv
python3 src/count_mentions.py data/output/base_dump.csv data/output/mention_counts.csv --n_workers=64
python3 src/find_top_articles.py data/output/mention_counts.csv data/output/top_articles.csv --ignore_dupes --n_workers=64
