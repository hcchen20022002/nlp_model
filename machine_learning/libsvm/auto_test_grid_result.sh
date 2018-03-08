#!/bin/bash
python tools/grid.py -t 1 training_data.scale > 0002_train/kernel_1_grid_result
python tools/grid.py -t 2 training_data.scale > 0002_train/kernel_2_grid_result
python tools/grid.py -t 3 training_data.scale > 0002_train/kernel_3_grid_result
