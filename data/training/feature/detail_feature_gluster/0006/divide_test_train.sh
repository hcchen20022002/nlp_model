#!/bin/bash

training_data='divide_train_set_'
test_data='data_set_'
divide_folder='divide_set_'

## divide data set
python3 smote_tool.py divide -I negative_feature_data -dp 10
python3 smote_tool.py divide -I positive_feature_data_orig -dp 10

## merge positive and negative data
for i in `seq 0 9` ;do
    rm -rf ${divide_folder}$i
    mkdir ${divide_folder}$i

    mv *_data_*$i ${divide_folder}$i
    cat ${divide_folder}$i/* > ${divide_folder}$i/${test_data}$i
done

## create training data by merge other divide part
for i in `seq 0 9` ;do
    for j in `seq 0 9` ;do
        if [ $j -ne $i ] ;then
            cat ${divide_folder}$j/${test_data}$j >> ${divide_folder}$i/${training_data}$i
        fi
    done
done

## scale test and training data
for i in `seq 0 9` ;do
    ../../../../../machine_learning/libsvm/svm-scale -l -1 -u 1 ${divide_folder}$i/${test_data}$i > ${divide_folder}$i/${test_data}$i'.scale'
    ../../../../../machine_learning/libsvm/svm-scale -l -1 -u 1 ${divide_folder}$i/${training_data}$i > ${divide_folder}$i/${training_data}$i'.scale'
done

## train
for i in `seq 0 9` ;do
    ../../../../../machine_learning/libsvm/svm-train -t 0 -w0 171 ${divide_folder}$i/${training_data}$i'.scale'
    mv ${training_data}$i'.scale.model' ${divide_folder}$i/${training_data}$i'.scale.model_kernel0'
    ../../../../../machine_learning/libsvm/svm-train -t 3 -w0 3.88 ${divide_folder}$i/${training_data}$i'.scale'
    mv ${training_data}$i'.scale.model' ${divide_folder}$i/${training_data}$i'.scale.model_kernel3'
done

## test
for i in `seq 0 9` ;do
    ../../../../../machine_learning/libsvm/svm-predict ${divide_folder}$i/${test_data}$i ${divide_folder}$i/${training_data}$i'.scale.model_kernel0' ${divide_folder}$i/'output_kernl0'
    ../../../../../machine_learning/libsvm/svm-predict ${divide_folder}$i/${test_data}$i ${divide_folder}$i/${training_data}$i'.scale.model_kernel3' ${divide_folder}$i/'output_kernl3'
done

## backfill
for i in `seq 0 9` ;do
    python3 smote_tool.py expansion  -I ${divide_folder}$i/${test_data}$i -ef ${divide_folder}$i/'output_kernl0' -O ${divide_folder}$i/${test_data}$i'_with_backfil'
    python3 smote_tool.py expansion  -I ${divide_folder}$i/${test_data}$i'_with_backfil' -ef ${divide_folder}$i/'output_kernl3' -O ${divide_folder}$i/${test_data}$i'_with_backfil'
done

## merga all
for i in `seq 0 9` ;do
    cat ${divide_folder}$i/${test_data}$i'_with_backfil' >> training_data_with_backfill
done
