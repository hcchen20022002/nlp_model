#!/usr/bin/bash

###### get original corpus
#python3 construct_corpus.py filter -I ../data/training/abstract_orig_text/positive/COPD_positive_orig_abstract.txt -F ../data/training/drug_list/drug.json -O ../data/training/corpus/positive_COPD.json

#python3 construct_corpus.py filter -I ../data/training/abstract_orig_text/positive/NSCLC_positive_orig_abstract.txt -F ../data/training/drug_list/drug.json -O ../data/training/corpus/positive_NSCLC.json

#python3 construct_corpus.py filter -I ../data/training/abstract_orig_text/negative/COPD_negative_orig_abstract.txt -F ../data/training/drug_list/drug.json -O ../data/training/corpus/negative_COPD.json

#python3 construct_corpus.py filter -I ../data/training/abstract_orig_text/negative/NSCLC_negative_orig_abstract.txt -F ../data/training/drug_list/drug.json -O ../data/training/corpus/negative_NSCLC.json

###### get parsing tree corpus
python3 construct_corpus.py get_tree -I ../data/training/corpus/negative_NSCLC.json -O ../data/training/corpus/negative_NSCLC_with_tree.json
#python3 construct_corpus.py get_tree -I ../data/training/corpus/negative_COPD.json -O ../data/training/corpus/negative_COPD_with_tree.json
python3 construct_corpus.py get_tree -I ../data/training/corpus/positive_NSCLC.json -O ../data/training/corpus/positive_NSCLC_with_tree.json
#python3 construct_corpus.py get_tree -I ../data/training/corpus/positive_COPD.json -O ../data/training/corpus/positive_COPD_with_tree.json

#python3 construct_corpus.py get_tree -I ../data/training/corpus/negative_NSCLC.json -O ../data/training/corpus/negative_NSCLC_with_tree.json
#python3 construct_corpus.py get_tree -I ../data/training/corpus/negative_COPD.json -O ../data/training/corpus/negative_COPD_with_tree.json
#python3 construct_corpus.py get_tree -I ../data/training/corpus/positive_NSCLC.json -O ../data/training/corpus/positive_NSCLC_with_tree.json
#python3 construct_corpus.py get_tree -I ../data/training/corpus/positive_COPD.json -O ../data/training/corpus/positive_COPD_with_tree.json
