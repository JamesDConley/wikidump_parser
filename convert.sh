python gen_csv.py $1 data/output/base_dump.csv
python count_mentions.py data/output/base_dump.csv data/output/mention_counts.csv --n_workers=64
python find_top_articles.py data/output/mention_counts.csv data/output/top_articles.csv --ignore_dupes
