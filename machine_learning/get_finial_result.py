#!/usr/bin/python

import sys, argparse

def get_sentence(file_name):
    with open(file_name, 'r') as f:
        sentences = []
        for line in f:
            sentences.append(line)
    return sentences

class RelevantData(object):
    def __init__(self, expect_data = [], real_data = []):
        self.TP, self.FP, self.FN, self.TN = 0.0, 0.0, 0.0, 0.0
        self.adviseT, self.effectT, self.intT, self.mechanismT = 0.0, 0.0, 0.0, 0.0
        self.adviseN, self.effectN, self.intN, self.mechanismN = 0.0, 0.0, 0.0, 0.0
        amount_of_data = len(expect_data)
        if len(real_data) !=  amount_of_data :
            print('Amount of expect result and real result cannot match!')
            exit()

        #tp_dict = [{'11':0,'12':0,'13':0,'14':0},
        #    {'21':0,'22':0,'23':0,'24':0},
        #    {'31':0,'32':0,'33':0,'34':0},
        #    {'41':0,'42':0,'43':0,'44':0}]
        true_tp_dict = {}
        false_tp_dict = {}
        fn_dict = {}
        fp_dict = {}
        for count in range(amount_of_data):
            real = real_data[count][0]
            expect = expect_data[count][0]
            if expect in ['1', '2', '3', '4']:
                #if real == expect:
                if real in ['1', '2', '3', '4']:
                    self.TP = self.TP + 1
                    if real == expect:
                        if expect in true_tp_dict:
                            true_tp_dict[expect] += 1
                        else:
                            true_tp_dict[expect] = 1
                    else:
                        if expect + real in false_tp_dict:
                            false_tp_dict[expect + real] += 1
                        else:
                            false_tp_dict[expect + real] = 1

                else:
                    self.FN = self.FN + 1
                    if expect in fn_dict:
                        fn_dict[expect] += 1
                    else:
                        fn_dict[expect] = 1

            elif expect == '0':
                if real == expect:
                    self.TN = self.TN + 1
                else:
                    if real in fp_dict:
                        fp_dict[real] += 1
                    else:
                        fp_dict[real] = 1
                    self.FP = self.FP + 1
        print('True TP dict: {0}'.format(true_tp_dict))
        print('False TP dict: {0}'.format(false_tp_dict))
        print('FN dict: {0}'.format(fn_dict))
        print('FP dict: {0}'.format(fp_dict))
        self.total = self.TP + self.FP + self.FN + self.TN
    def accuracy(self):
        return (self.TP + self.TN)/ self.total
    def pprecision(self):
        return self.TP / (self.TP + self.FP)
    def precall(self):
        return self.TP / (self.TP + self.FN)
    def pF1(self):
        return self.TP*2 / (self.TP*2 + self.FP + self.FN)
    def nprecision(self):
        return self.TN / (self.TN + self.FN)
    def nrecall(self):
        return self.TN / (self.TN + self.FP)
    def nF1(self):
        return self.TN*2 / (self.TN*2 + self.FP + self.FN)
    #def nF1(self):
    #    return self.TN*2 / (self.TN*2 + self.FP + self.FN)


if '__main__' == __name__ :
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('option', choices=['all', 'accuracy', 'precision', 'recall', 'F1'], help='provide a action you want to do')
    # cat ${test file} | cut -d' ' -f1 > ${expected result}
    parser.add_argument('-e', '--expect', type=str, default='INPUT_FILE', help='provide a file which record the result you expect')
    parser.add_argument('-r', '--real', type=str, default='INPUT_FILE', help='provide a file which record real result you get')

    opt = parser.parse_args(sys.argv[1:])

    expect_data = get_sentence(opt.expect)
    real_data = get_sentence(opt.real)
    relevant_data = RelevantData(expect_data, real_data)
    print('TP : {0}'.format(relevant_data.TP))
    print('FP : {0}'.format(relevant_data.FP))
    print('FN : {0}'.format(relevant_data.FN))
    print('TN : {0}'.format(relevant_data.TN))
    print('Total : {0}'.format(relevant_data.total))
    print('')

    if 'accuracy' == opt.option:
        print(relevant_data.accuracy())
    elif 'precision' == opt.option:
        print(relevant_data.precision())
    elif 'recall' == opt.option:
        print(relevant_data.recall())
    elif 'F1' == opt.option:
        print(relevant_data.F1())
    elif 'all' == opt.option:
        print('Accuracy : {0}'.format(relevant_data.accuracy()))
        print('')
        print('Positive Precision : {0}'.format(relevant_data.pprecision()))
        print('Negative Precision : {0}'.format(relevant_data.nprecision()))
        print('')
        print('Positive Recall : {0}'.format(relevant_data.precall()))
        print('Negative Recall : {0}'.format(relevant_data.nrecall()))
        print('')
        print('Positve F1 : {0}'.format(relevant_data.pF1()))
        print('Negative F1 : {0}'.format(relevant_data.nF1()))
        print('')
    #    print('Negative F1 : {0}'.format(relevant_data.nF1()))
