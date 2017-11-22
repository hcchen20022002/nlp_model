#!/usr/bin/python3
# coding=UTF-8

import sys, argparse, json

class feature_set(object):
    def __init__(self, input_file):
        # features would be transform to a list with dict
        # each dict is one of data
        self.data_set, self.max_feature = self.get_data(input_file)

    def get_data(self, input_file):
        data_list = []
        max_feature = 0
        with open(input_file, 'r') as f:
            for line in f:
                feature_dict = {}
                tmp_wd = ''
                tmp_key = ''
                wd_count = 0
                for wd in line:
                    wd_count += 1
                    if ':' == wd:
                        tmp_key = tmp_wd
                        tmp_wd = ''
                    elif ' ' == wd or wd_count == len(line):
                        tmp_key = 0 if not tmp_key else tmp_key
                        feature_dict[int(tmp_key)] = int(tmp_wd)
                        tmp_wd = ''
                        tmp_key = ''
                    else:
                        tmp_wd += wd
                if max(feature_dict) >= max_feature:
                    max_feature = max(feature_dict)
                data_list.append(feature_dict)
        return data_list, max_feature

    def do_smote(self, ignore_list = []):
        new_data_set = []
        for main_data in self.data_set:
            for secondary_data in self.data_set:
                if main_data != secondary_data:
                    new_data = {}
                    for feature in main_data:
                        new_data[feature] = main_data[feature]\
                                if feature in ignore_list\
                                else int((main_data[feature] + secondary_data[feature])/2)
                    new_data_set.append(new_data)
        return new_data_set

    def do_decrease(self, target_number = 1000):
        import random
        random.shuffle(self.data_set)
        return self.data_set[0:target_number]

def write_new_data_set(output_file, data_set, max_feature):
    with open(output_file, 'w') as output_f:
        for data in data_set:
            output_f.write('{0}'.format(data[0]))
            for _ in range(1, (max_feature + 1)):
                output_f.write(' {0}:{1}'.format(_, data[_]))
            output_f.write('\n')
    return True

if '__main__' == __name__:
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('option', choices=['increase', 'decrease'], help='provide a action you want to do')
    parser.add_argument('-I', '--Input', type=str, default='INPUT', help='provide a feature test with libsvm format')
    parser.add_argument('-O', '--Output', type=str, default='OUTPUT', help='provide a file to save output')
    parser.add_argument('-t', '--target-number', type=int, default=1000, help='provide a number to decrease features')
    parser.add_argument('-i', '--ignore-list', type=str, default='1,2,3,4', help='provide a list of number which features would be ignore to change')
    opt = parser.parse_args(sys.argv[1:])

    orig_data = feature_set(opt.Input)

    if 'increase' == opt.option:
        #TODO need to fix ignore list became user can input
        ignore_list = [3,4,5,6,7,9,11,12,13,14,15,17]
        data_set_with_smote = orig_data.do_smote(ignore_list)
        write_new_data_set(opt.Output, data_set_with_smote, orig_data.max_feature)
    if 'decrease' == opt.option:
        data_set_decrease = orig_data.do_decrease(opt.target_number)
        write_new_data_set(opt.Output, data_set_decrease, orig_data.max_feature)

