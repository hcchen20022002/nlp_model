#! /bin/bash


#test_comand="./svm-predict test_data.scale training_data.scale.model output"

#training_comand(){
#}

##### Stage 1 ###################################
./svm-train -t 0 training_data.scale
mv training_data.scale.model  0005_train/stage1/kernel_0/

./svm-train -t 1 training_data.scale
mv training_data.scale.model  0005_train/stage1/kernel_1_g_0_c_0/

./svm-train training_data.scale
mv training_data.scale.model  0005_train/stage1/kernel_2_g_0_c_0/

./svm-train -t 3 training_data.scale
mv training_data.scale.model  0005_train/stage1/kernel_3_g_0_c_0/

./svm-predict test_data.scale 0005_train/stage1/kernel_0/training_data.scale.model 0005_train/stage1/kernel_0/output
./svm-predict test_data.scale 0005_train/stage1/kernel_1_g_0_c_0/training_data.scale.model 0005_train/stage1/kernel_1_g_0_c_0/output
./svm-predict test_data.scale 0005_train/stage1/kernel_2_g_0_c_0/training_data.scale.model 0005_train/stage1/kernel_2_g_0_c_0/output
./svm-predict test_data.scale 0005_train/stage1/kernel_3_g_0_c_0/training_data.scale.model 0005_train/stage1/kernel_3_g_0_c_0/output

./svm-predict training_data.scale 0005_train/stage1/kernel_0/training_data.scale.model 0005_train/stage1/kernel_0/training_output
./svm-predict training_data.scale 0005_train/stage1/kernel_1_g_0_c_0/training_data.scale.model 0005_train/stage1/kernel_1_g_0_c_0/training_output
./svm-predict training_data.scale 0005_train/stage1/kernel_2_g_0_c_0/training_data.scale.model 0005_train/stage1/kernel_2_g_0_c_0/training_output
./svm-predict training_data.scale 0005_train/stage1/kernel_3_g_0_c_0/training_data.scale.model 0005_train/stage1/kernel_3_g_0_c_0/training_output

##### expansion #################################
python3 ../../create_corpus/smote_tool.py expansion -I training_data.scale -ef 0005_train/stage1/kernel_0/training_output -O 0005_train/stage2/kernel_0/training_data_plus_k0.scale
python3 ../../create_corpus/smote_tool.py expansion -I training_data.scale -ef 0005_train/stage1/kernel_1_g_0_c_0/training_output -O 0005_train/stage2/kernel_1/training_data_plus_k1.scale
python3 ../../create_corpus/smote_tool.py expansion -I training_data.scale -ef 0005_train/stage1/kernel_2_g_0_c_0/training_output -O 0005_train/stage2/kernel_2/training_data_plus_k2.scale
python3 ../../create_corpus/smote_tool.py expansion -I training_data.scale -ef 0005_train/stage1/kernel_3_g_0_c_0/training_output -O 0005_train/stage2/kernel_3/training_data_plus_k3.scale

python3 ../../create_corpus/smote_tool.py expansion -I training_data.scale -ef 0005_train/stage1/kernel_0/training_output -O 0005_train/stage2/kernel_all/training_data_plus_kAll.scale
python3 ../../create_corpus/smote_tool.py expansion -I 0005_train/stage2/kernel_all/training_data_plus_kAll.scale -ef 0005_train/stage1/kernel_1_g_0_c_0/training_output -O 0005_train/stage2/kernel_all/training_data_plus_kAll.scale
python3 ../../create_corpus/smote_tool.py expansion -I 0005_train/stage2/kernel_all/training_data_plus_kAll.scale -ef 0005_train/stage1/kernel_2_g_0_c_0/training_output -O 0005_train/stage2/kernel_all/training_data_plus_kAll.scale
python3 ../../create_corpus/smote_tool.py expansion -I 0005_train/stage2/kernel_all/training_data_plus_kAll.scale -ef 0005_train/stage1/kernel_3_g_0_c_0/training_output -O 0005_train/stage2/kernel_all/training_data_plus_kAll.scale

python3 ../../create_corpus/smote_tool.py expansion -I test_data.scale -ef 0005_train/stage1/kernel_0/output -O 0005_train/stage2/kernel_0/test_data_plus_k0.scale
python3 ../../create_corpus/smote_tool.py expansion -I test_data.scale -ef 0005_train/stage1/kernel_1_g_0_c_0/output -O 0005_train/stage2/kernel_1/test_data_plus_k1.scale
python3 ../../create_corpus/smote_tool.py expansion -I test_data.scale -ef 0005_train/stage1/kernel_2_g_0_c_0/output -O 0005_train/stage2/kernel_2/test_data_plus_k2.scale
python3 ../../create_corpus/smote_tool.py expansion -I test_data.scale -ef 0005_train/stage1/kernel_3_g_0_c_0/output -O 0005_train/stage2/kernel_3/test_data_plus_k3.scale

python3 ../../create_corpus/smote_tool.py expansion -I test_data.scale -ef 0005_train/stage1/kernel_0/output -O 0005_train/stage2/kernel_all/test_data_plus_kAll.scale
python3 ../../create_corpus/smote_tool.py expansion -I 0005_train/stage2/kernel_all/test_data_plus_kAll.scale -ef 0005_train/stage1/kernel_1_g_0_c_0/output -O 0005_train/stage2/kernel_all/test_data_plus_kAll.scale
python3 ../../create_corpus/smote_tool.py expansion -I 0005_train/stage2/kernel_all/test_data_plus_kAll.scale -ef 0005_train/stage1/kernel_2_g_0_c_0/output -O 0005_train/stage2/kernel_all/test_data_plus_kAll.scale
python3 ../../create_corpus/smote_tool.py expansion -I 0005_train/stage2/kernel_all/test_data_plus_kAll.scale -ef 0005_train/stage1/kernel_3_g_0_c_0/output -O 0005_train/stage2/kernel_all/test_data_plus_kAll.scale
##### Stage 2 ###################################
./svm-train -t 0 0005_train/stage2/kernel_0/training_data_plus_k0.scale
mv training_data_plus_k0.scale.model 0005_train/stage2/kernel_0/training_data_plus_k0.scale.kernel0.model

./svm-train -t 1 0005_train/stage2/kernel_0/training_data_plus_k0.scale
mv training_data_plus_k0.scale.model 0005_train/stage2/kernel_0/training_data_plus_k0.scale.kernel1.model

./svm-train -t 2 0005_train/stage2/kernel_0/training_data_plus_k0.scale
mv training_data_plus_k0.scale.model 0005_train/stage2/kernel_0/training_data_plus_k0.scale.kernel2.model

./svm-train -t 3 0005_train/stage2/kernel_0/training_data_plus_k0.scale
mv training_data_plus_k0.scale.model 0005_train/stage2/kernel_0/training_data_plus_k0.scale.kernel3.model

./svm-predict 0005_train/stage2/kernel_0/test_data_plus_k0.scale 0005_train/stage2/kernel_0/training_data_plus_k0.scale.kernel0.model 0005_train/stage2/kernel_0/data_plus_k0_kernel0_output
./svm-predict 0005_train/stage2/kernel_0/test_data_plus_k0.scale 0005_train/stage2/kernel_0/training_data_plus_k0.scale.kernel1.model 0005_train/stage2/kernel_0/data_plus_k0_kernel1_output
./svm-predict 0005_train/stage2/kernel_0/test_data_plus_k0.scale 0005_train/stage2/kernel_0/training_data_plus_k0.scale.kernel2.model 0005_train/stage2/kernel_0/data_plus_k0_kernel2_output
./svm-predict 0005_train/stage2/kernel_0/test_data_plus_k0.scale 0005_train/stage2/kernel_0/training_data_plus_k0.scale.kernel3.model 0005_train/stage2/kernel_0/data_plus_k0_kernel3_output

./svm-train -t 0 0005_train/stage2/kernel_1/training_data_plus_k1.scale
mv training_data_plus_k1.scale.model 0005_train/stage2/kernel_1/training_data_plus_k1.scale.kernel0.model

./svm-train -t 1 0005_train/stage2/kernel_1/training_data_plus_k1.scale
mv training_data_plus_k1.scale.model 0005_train/stage2/kernel_1/training_data_plus_k1.scale.kernel1.model

./svm-train -t 2 0005_train/stage2/kernel_1/training_data_plus_k1.scale
mv training_data_plus_k1.scale.model 0005_train/stage2/kernel_1/training_data_plus_k1.scale.kernel2.model

./svm-train -t 3 0005_train/stage2/kernel_1/training_data_plus_k1.scale
mv training_data_plus_k1.scale.model 0005_train/stage2/kernel_1/training_data_plus_k1.scale.kernel3.model

./svm-predict 0005_train/stage2/kernel_1/test_data_plus_k1.scale 0005_train/stage2/kernel_1/training_data_plus_k1.scale.kernel0.model 0005_train/stage2/kernel_1/data_plus_k1_kernel0_output
./svm-predict 0005_train/stage2/kernel_1/test_data_plus_k1.scale 0005_train/stage2/kernel_1/training_data_plus_k1.scale.kernel1.model 0005_train/stage2/kernel_1/data_plus_k1_kernel1_output
./svm-predict 0005_train/stage2/kernel_1/test_data_plus_k1.scale 0005_train/stage2/kernel_1/training_data_plus_k1.scale.kernel2.model 0005_train/stage2/kernel_1/data_plus_k1_kernel2_output
./svm-predict 0005_train/stage2/kernel_1/test_data_plus_k1.scale 0005_train/stage2/kernel_1/training_data_plus_k1.scale.kernel3.model 0005_train/stage2/kernel_1/data_plus_k1_kernel3_output

./svm-train -t 0 0005_train/stage2/kernel_2/training_data_plus_k2.scale
mv training_data_plus_k2.scale.model 0005_train/stage2/kernel_2/training_data_plus_k2.scale.kernel0.model

./svm-train -t 1 0005_train/stage2/kernel_2/training_data_plus_k2.scale
mv training_data_plus_k2.scale.model 0005_train/stage2/kernel_2/training_data_plus_k2.scale.kernel1.model

./svm-train -t 2 0005_train/stage2/kernel_2/training_data_plus_k2.scale
mv training_data_plus_k2.scale.model 0005_train/stage2/kernel_2/training_data_plus_k2.scale.kernel2.model

./svm-train -t 3 0005_train/stage2/kernel_2/training_data_plus_k2.scale
mv training_data_plus_k2.scale.model 0005_train/stage2/kernel_2/training_data_plus_k2.scale.kernel3.model

./svm-predict 0005_train/stage2/kernel_2/test_data_plus_k2.scale 0005_train/stage2/kernel_2/training_data_plus_k2.scale.kernel0.model 0005_train/stage2/kernel_2/data_plus_k2_kernel0_output
./svm-predict 0005_train/stage2/kernel_2/test_data_plus_k2.scale 0005_train/stage2/kernel_2/training_data_plus_k2.scale.kernel1.model 0005_train/stage2/kernel_2/data_plus_k2_kernel1_output
./svm-predict 0005_train/stage2/kernel_2/test_data_plus_k2.scale 0005_train/stage2/kernel_2/training_data_plus_k2.scale.kernel2.model 0005_train/stage2/kernel_2/data_plus_k2_kernel2_output
./svm-predict 0005_train/stage2/kernel_2/test_data_plus_k2.scale 0005_train/stage2/kernel_2/training_data_plus_k2.scale.kernel3.model 0005_train/stage2/kernel_2/data_plus_k2_kernel3_output

./svm-train -t 0 0005_train/stage2/kernel_3/training_data_plus_k3.scale
mv training_data_plus_k3.scale.model 0005_train/stage2/kernel_3/training_data_plus_k3.scale.kernel0.model

./svm-train -t 1 0005_train/stage2/kernel_3/training_data_plus_k3.scale
mv training_data_plus_k3.scale.model 0005_train/stage2/kernel_3/training_data_plus_k3.scale.kernel1.model

./svm-train -t 2 0005_train/stage2/kernel_3/training_data_plus_k3.scale
mv training_data_plus_k3.scale.model 0005_train/stage2/kernel_3/training_data_plus_k3.scale.kernel2.model

./svm-train -t 3 0005_train/stage2/kernel_3/training_data_plus_k3.scale
mv training_data_plus_k3.scale.model 0005_train/stage2/kernel_3/training_data_plus_k3.scale.kernel3.model

./svm-predict 0005_train/stage2/kernel_3/test_data_plus_k3.scale 0005_train/stage2/kernel_3/training_data_plus_k3.scale.kernel0.model 0005_train/stage2/kernel_3/data_plus_k3_kernel0_output
./svm-predict 0005_train/stage2/kernel_3/test_data_plus_k3.scale 0005_train/stage2/kernel_3/training_data_plus_k3.scale.kernel1.model 0005_train/stage2/kernel_3/data_plus_k3_kernel1_output
./svm-predict 0005_train/stage2/kernel_3/test_data_plus_k3.scale 0005_train/stage2/kernel_3/training_data_plus_k3.scale.kernel2.model 0005_train/stage2/kernel_3/data_plus_k3_kernel2_output
./svm-predict 0005_train/stage2/kernel_3/test_data_plus_k3.scale 0005_train/stage2/kernel_3/training_data_plus_k3.scale.kernel3.model 0005_train/stage2/kernel_3/data_plus_k3_kernel3_output

./svm-train -t 0 0005_train/stage2/kernel_all/training_data_plus_kAll.scale
mv training_data_plus_kAll.scale.model 0005_train/stage2/kernel_all/training_data_plus_kAll.scale.kernel0.model

./svm-train -t 1 0005_train/stage2/kernel_all/training_data_plus_kAll.scale
mv training_data_plus_kAll.scale.model 0005_train/stage2/kernel_all/training_data_plus_kAll.scale.kernel1.model

./svm-train -t 2 0005_train/stage2/kernel_all/training_data_plus_kAll.scale
mv training_data_plus_kAll.scale.model 0005_train/stage2/kernel_all/training_data_plus_kAll.scale.kernel2.model

./svm-train -t 3 0005_train/stage2/kernel_all/training_data_plus_kAll.scale
mv training_data_plus_kAll.scale.model 0005_train/stage2/kernel_all/training_data_plus_kAll.scale.kernel3.model

./svm-predict 0005_train/stage2/kernel_all/test_data_plus_kAll.scale 0005_train/stage2/kernel_all/training_data_plus_kAll.scale.kernel0.model 0005_train/stage2/kernel_all/data_plus_kAll_kernel0_output
./svm-predict 0005_train/stage2/kernel_all/test_data_plus_kAll.scale 0005_train/stage2/kernel_all/training_data_plus_kAll.scale.kernel1.model 0005_train/stage2/kernel_all/data_plus_kAll_kernel1_output
./svm-predict 0005_train/stage2/kernel_all/test_data_plus_kAll.scale 0005_train/stage2/kernel_all/training_data_plus_kAll.scale.kernel2.model 0005_train/stage2/kernel_all/data_plus_kAll_kernel2_output
./svm-predict 0005_train/stage2/kernel_all/test_data_plus_kAll.scale 0005_train/stage2/kernel_all/training_data_plus_kAll.scale.kernel3.model 0005_train/stage2/kernel_all/data_plus_kAll_kernel3_output

