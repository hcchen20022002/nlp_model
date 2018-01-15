#!/usr/bin/bash

python3 construct_corpus.py get_tree -I medline.json -O medline_with_tree.json
python3 construct_corpus.py get_tree -I drugbank.json -O drugbank_with_tree.json
