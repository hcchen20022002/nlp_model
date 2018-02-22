#! /bin/bash


#test_comand="./svm-predict test_data.scale training_data.scale.model output"

#training_comand(){
#}

./svm-train -t 0 training_data.scale
mv training_data.scale.model  0001_train/kernel_0/

./svm-train -t 1 training_data.scale
mv training_data.scale.model  0001_train/kernel_1_g_0_c_0/

./svm-train training_data.scale
mv training_data.scale.model  0001_train/kernel_2_g_0_c_0/

./svm-train -t 3 training_data.scale
mv training_data.scale.model  0001_train/kernel_3_g_0_c_0/


./svm-predict test_data.scale 0001_train/kernel_0/training_data.scale.model 0001_train/kernel_0/output
./svm-predict test_data.scale 0001_train/kernel_1_g_0_c_0/training_data.scale.model 0001_train/kernel_1_g_0_c_0/output
./svm-predict test_data.scale 0001_train/kernel_2_g_0_c_0/training_data.scale.model 0001_train/kernel_2_g_0_c_0/output
./svm-predict test_data.scale  0001_train/kernel_3_g_0_c_0/training_data.scale.model 0001_train/kernel_3_g_0_c_0/output
