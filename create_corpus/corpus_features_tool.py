#!/usr/bin/python3
# coding=UTF-8

import sys, argparse, json, time

def get_info(json_file = ""):
    with open(json_file) as json_f:
        contents = json.load(json_f)
    print('quantity of data: {0}'.format(len(contents)))
    positive_count = 0
    negative_count = 0
    for _ in contents:
#        print('Disease: {0}'.format(_['disease']))
#        print('Drug: {0}'.format(_['drug']))
#        print('Polarity: {0}'.format(_['polarity']))
#        print('Original Sentens: {0}'.format(_['orig_sen']))
#        print('__________________________________________________')
        if _['polarity'] == 1:
            positive_count = positive_count + 1
        elif _['polarity'] == 0:
            negative_count = negative_count + 1
            if _['drug'] == 'indacaterol':
                print(_['orig_sen'])
                print('_____________________________________________________')
    print('Positive value: {0}'.format(positive_count))
    print('negative value: {0}'.format(negative_count))
    return True


if '__main__' == __name__ :
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('option', choices=['info'], help='provide a action you want to do')
    parser.add_argument('-I', '--Input', type=str, default='INPUT', help='provide a input text')
    parser.add_argument('-O', '--Output', type=str, default='OUTPUT', help='provide a file to save output')
    opt = parser.parse_args(sys.argv[1:])

    if 'info' == opt.option:
        get_info(opt.Input)
