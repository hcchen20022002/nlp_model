#!/bin/sh

training_data_file='training_data'
test_data_file='test_data'
rm ${training_data_file}* ${test_data_file}*
#numa=0
num=1
numa=1
numb=1
numc=1
for i in $(seq 1 1000) ;do
    num=$((RANDOM%5000))
    echo "1 1:${num} 2:$((num*num))" >> ${training_data_file}
    echo "2 1:${num} 2:$((num*2))" >> ${training_data_file}
    echo "3 1:${num} 2:$((num+i))" >> ${training_data_file}
    num=$((RANDOM%5000))
    echo "1 1:${num} 2:$((num*num))" >> ${test_data_file}
    echo "2 1:${num} 2:$((num*2))" >> ${test_data_file}
    echo "3 1:${num} 2:$((num+i))" >> ${test_data_file}
    #numa=$((numa*2))
    #numb=$((numb*3))
    #numc=$((numc*5))
## linear test data, numa = 0, numb = 1
#    echo "1 1:$((numa + i*2))" >> ${training_data_file}
#    echo "2 1:$((numa + i*2 + 2000))" >> ${training_data_file}
#    echo "3 1:$((numa + i*2 + 4000))" >> ${training_data_file}
#    echo "1 1:$((numb + i*2))" >> ${test_data_file}
#    echo "2 1:$((numb + i*2 + 2000))" >> ${test_data_file}
#    echo "3 1:$((numb + i*2 + 4000))" >> ${test_data_file}

## randon test data
#    echo "1 1:$((0 + $RANDOM % 10000))" >> ${training_data_file}
#    echo "2 1:$((10001 + $RANDOM % 10000))" >> ${training_data_file}
#    echo "3 1:$((20001 + $RANDOM % 10000))" >> ${training_data_file}
done
./svm-scale -l -1 -u 1 -s range ${training_data_file} > ${training_data_file}_scale
./svm-scale -l -1 -u 1 -s range ${test_data_file} > ${test_data_file}_scale
#./svm-train ${training_data_file}
#./svm-predict ${test_data_file} ${training_data_file}.model output
