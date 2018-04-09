#!/usr/bin/python3
# coding=UTF-8

import sys, argparse, json

class feature_data_set(object):
    def __init__(self, input_file = ''):
        # features would be transform to a list with dict
        # each dict is one of data
        if input_file:
            self.data_set, self.max_feature = self.get_data(input_file)
        else:
            self.data_set = []
            self.max_feature = 0

    def get_data(self, input_file):
        data_list = []
        max_feature = 0
        with open(input_file, 'r') as f:
            for line in f:
                feature_dict = {}
                tmp_wd, tmp_key, wd_count = '', '', 0
                for wd in line:
                    wd_count += 1
                    if ':' == wd:
                        tmp_key = tmp_wd
                        tmp_wd = ''
                    elif ' ' == wd or wd_count == len(line)-1:
                        if  wd_count == len(line)-1:
                            tmp_wd += wd
                        tmp_key = 0 if not tmp_key else tmp_key
                        feature_dict[int(tmp_key)] = float(tmp_wd)
                        tmp_wd, tmp_key = '', ''
                    else:
                        tmp_wd += wd
                if max(feature_dict) >= max_feature:
                    max_feature = max(feature_dict)
                data_list.append(feature_dict)
        return data_list, max_feature

    def do_smote(self, k_near_node = 1, ignore_list = []):
        import random
        new_data_set = []
        for main_data in self.data_set:
            secondary_data_set = list(self.data_set)
            random.shuffle(secondary_data_set)
            distance_list = []
            nearest_node_list = []
            for secondary_data in secondary_data_set:
                distance = self._node_distance(main_data, secondary_data)
                if 0 < distance and distance not in distance_list:
                    distance_list.append(distance)
                    nearest_node_list.append(secondary_data)
            smote_point_list = sorted(zip(distance_list, nearest_node_list))[:k_near_node]
            for smote_point in smote_point_list:
                new_data = {}
                for feature in main_data:
                    new_data[feature] = main_data[feature]\
                            if feature in ignore_list\
                            else float((main_data[feature] + smote_point[1][feature])/2)
                print(new_data)
                new_data_set.append(new_data)
        return new_data_set

    def do_decrease(self, target_number = 1000):
        import random
        random.shuffle(self.data_set)
        return self.data_set[0:target_number]

    def expansion_features(self, feature_set = list()):
        if len(feature_set) != len(self.data_set):
            print('Data volume not match:')
            print('Input:{0}'.format(len(self.data_set)))
            print('Expansion feature:{0}'.format(len(feature_set)))
            return False
        self.max_feature += 1
        for i in range(0,len(self.data_set)):
            self.data_set[i][self.max_feature] = int(feature_set[i]) if int(feature_set[i]) != self.data_set[i][0] else -1
        return True

    def divide_data_set(self, divided_part = 10):
        amount_of_data_in_part = int(len(self.data_set)/divided_part)
        print(amount_of_data_in_part)
        divided_data_set_list = []
        for number in range(0, divided_part):
            part_data_set = feature_data_set()
            part_data_set.max_feature = self.max_feature
            part_data_set.data_set = self.data_set[
                    (number*amount_of_data_in_part):((number+1)*(amount_of_data_in_part))]
            divided_data_set_list.append(part_data_set)

        divided_data_set_list[-1].data_set += self.data_set[
                (divided_part*amount_of_data_in_part):]
        return divided_data_set_list

    def _node_distance(self, nodeA, nodeB):
        if len(nodeA) != len(nodeB):
            print('{0}, {1} should be same lenght')
            exit()
        if nodeA == nodeB:
            return 0 
        sum_result = 0
        for index in range(0, len(nodeA)):
            sum_result += (nodeA[index] - nodeB[index])**2
        return sum_result**0.5

class expansion_feature_set(object):
    def __init__(self, input_file):
        self.feature_set = self.get_features(input_file)
    def get_features(self, input_file):
        feature_list = []
        with open(input_file, 'r') as f:
            for line in f:
                feature_list.append(int(line))
        return feature_list


def write_new_data_set(output_file, data_set, max_feature):
    with open(output_file, 'w') as output_f:
        for data in data_set:
            output_f.write('{0}'.format(data[0]))
            for _ in range(1, (max_feature + 1)):
                if _ in data:
                    output_f.write(' {0}:{1}'.format(_, data[_]))
            output_f.write('\n')
    return True


if '__main__' == __name__:
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('option', choices=['increase', 'decrease', 'expansion', 'divide'], help='provide a action you want to do')
    parser.add_argument('-I', '--Input', type=str, default='INPUT', help='provide a feature test with libsvm format')
    parser.add_argument('-O', '--Output', type=str, default='OUTPUT', help='provide a file to save output')

    increase_parser = parser.add_argument_group('increase: increase data in features data set by smote algorithm')
    increase_parser.add_argument('-il', '--ignore-list', type=str, default='1,2,3,4', help='provide a list of number which features would be ignore to change')
    increase_parser.add_argument('-kn', '--k-nearest', type=int, default=1, help='provide a list of number which features would be ignore to change')

    decrease_parser = parser.add_argument_group('decrease: decrease data in features data set by random')
    decrease_parser.add_argument('-t', '--target-number', type=int, default=1000, help='provide a number to decrease features')

    expansion_parser = parser.add_argument_group('expansion: expansion feature to data from another data set. (two data set must have equal quantity of data)')
    expansion_parser.add_argument('-ef', '--expansion-file', type=str, default='expansion_feature', help='provide a number to decrease features')

    divide_parser = parser.add_argument_group('divide: divided data set to N parts')
    divide_parser.add_argument('-dp', '--divided-part', type=int, default=10, help='provide a number parts you want to divided')

    opt = parser.parse_args(sys.argv[1:])

    orig_data = feature_data_set(opt.Input)

    if 'increase' == opt.option:
        #TODO need to fix ignore list became user can input
        #ignore_list = [3,4,5,6,7,9,11,13,15,17]
        ignore_list = []
        data_set_with_smote = orig_data.do_smote(opt.k_nearest, ignore_list)
        write_new_data_set(opt.Output, data_set_with_smote, orig_data.max_feature)
    if 'decrease' == opt.option:
        data_set_decrease = orig_data.do_decrease(opt.target_number)
        write_new_data_set(opt.Output, data_set_decrease, orig_data.max_feature)
    if 'expansion' == opt.option:
        new_feature = expansion_feature_set(opt.expansion_file)
        if orig_data.expansion_features(new_feature.feature_set):
            write_new_data_set(opt.Output, orig_data.data_set, orig_data.max_feature)
    if 'divide' == opt.option:
        data_set_divided_list = orig_data.divide_data_set(opt.divided_part)
        for number in range(0, opt.divided_part):
            write_new_data_set('{0}_{1}'.format(opt.Input, number),
                    data_set_divided_list[number].data_set,
                    data_set_divided_list[number].max_feature)
