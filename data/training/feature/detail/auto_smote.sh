#!/bin/bash

python3 smote_tool.py increase -kn 27 -I 0004/advise_type_data_set -O 0004/advise_type_smote_data_set
python3 smote_tool.py increase -kn 13 -I 0004/effect_type_data_set -O 0004/effect_type_smote_data_set
python3 smote_tool.py increase -kn 126 -I 0004/int_type_data_set -O 0004/int_type_smote_data_set
python3 smote_tool.py increase -kn 17 -I 0004/mechanism_type_data_set -O 0004/mechanism_type_smote_data_set
