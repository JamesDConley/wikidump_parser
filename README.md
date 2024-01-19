# Wikidump Parser

A toolkit for extracting article text from wikipedia dumps.

Features include
- [x] Extracting article names, basic metadata, and article wikitext
- [x] Identifying other articles mentioned in each article (Useful for graphs!)
- [ ] Sorting the article data by mentions  # Needs Cleanup
- [ ] Simplifying the wikitext contents # Needs Cleanup
- [ ] Creating a memory mapped object for efficient random access of text  # Needs Cleanup

See convert.sh for example usage

# Note on Functionality
I'm cobbling this repo together from several scripts and notebooks I put together.
As of this commit I have not tested the individual scripts or the `convert.sh` but I plan to debug on a new wikipedia dump once it finishes downloading.

Feel free to put in issues for requests/help

Thanks for reading :) 