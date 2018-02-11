#! /bin/bash


#test_comand="./svm-predict test_data.scale training_data.scale.model output"

#training_comand(){
#}

#./svm-train -t 0 training_data.scale
#mv training_data.scale.model  training_data.scale.kernel_0.model


./svm-train -t 1 training_data.scale
mv training_data.scale.model  training_data.scale.kernel_1.model

./svm-train -t 3 training_data.scale
mv training_data.scale.model  training_data.scale.kernel_3.model
