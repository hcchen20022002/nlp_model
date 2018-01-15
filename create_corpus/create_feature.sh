#!/usr/bin/bash

python3 corpus_features_tool.py create -f all -I ../data/test/corpus/positive_HC_with_tree.json
python3 corpus_features_tool.py create -f all -I ../data/test/corpus/positive_IC_with_tree.json
python3 corpus_features_tool.py create -f all -I ../data/test/corpus/negative_IC_with_tree.json

mv all_type_* ../data/test/feature/detail_feature_gluster/0001/
